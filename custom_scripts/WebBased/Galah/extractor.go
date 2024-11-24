package main

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

type LogEntry struct {
	Error        *Error        `json:"error,omitempty"`
	EventTime    string        `json:"eventTime"`
	SrcIP        string        `json:"srcIP"`
	HttpRequest  *HttpRequest  `json:"httpRequest,omitempty"`
	HttpResponse *HttpResponse `json:"httpResponse,omitempty"`
}

type Error struct {
	Msg string `json:"msg"`
}

type HttpRequest struct {
	Body    string `json:"body"`
	Method  string `json:"method"`
	Request string `json:"request"`
}

type HttpResponse struct {
	Body string `json:"body"`
}

func main() {
	// Define flags for input and output directories
	outputPath := flag.String("output", "output/combined.csv", "Path to the output CSV file")
	flag.Parse()

	// List of input JSON files
	inputFiles := []string{
		"galah_DO.json",
	}

	// Create the output folder if it doesn't exist
	outputDir := filepath.Dir(*outputPath)
	if err := os.MkdirAll(outputDir, os.ModePerm); err != nil {
		fmt.Printf("Error creating output directory '%s': %v\n", outputDir, err)
		return
	}

	// Open output CSV file
	outputFile, err := os.Create(*outputPath)
	if err != nil {
		fmt.Printf("Error creating output file '%s': %v\n", *outputPath, err)
		return
	}
	defer outputFile.Close()

	writer := csv.NewWriter(outputFile)
	defer writer.Flush()

	// Write the CSV header
	header := []string{"EventTime", "SrcIP", "HasError", "Request Body", "Method", "Request Path", "Response Body"}
	if err := writer.Write(header); err != nil {
		fmt.Printf("Error writing header to CSV: %v\n", err)
		return
	}

	count := 0

	// Loop through each input file
	for _, inputFile := range inputFiles {
		file, err := os.Open(inputFile)
		if err != nil {
			fmt.Printf("Error opening input file '%s': %v\n", inputFile, err)
			continue
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		lineNumber := 0

		for scanner.Scan() {
			lineNumber++
			line := scanner.Text()
			var entry LogEntry

			// Parse the JSON entry
			if err := json.Unmarshal([]byte(line), &entry); err != nil {
				fmt.Printf("Error parsing JSON on line %d in file '%s': %v\nLine Content: %s\n", lineNumber, inputFile, err, line)
				continue
			}

			// Extract fields from the log entry
			hasError := "false"
			if entry.Error != nil {
				hasError = "true"
			}

			requestBody := ""
			method := ""
			requestPath := ""
			if entry.HttpRequest != nil {
				requestBody = entry.HttpRequest.Body
				method = entry.HttpRequest.Method
				requestPath = entry.HttpRequest.Request
			}

			responseBody := ""
			if entry.HttpResponse != nil {
				responseBody = entry.HttpResponse.Body
			}

			// Write the row to CSV
			row := []string{
				entry.EventTime,
				entry.SrcIP,
				hasError,
				requestBody,
				method,
				requestPath,
				responseBody,
			}

			if err := writer.Write(row); err != nil {
				fmt.Printf("Error writing row to CSV on line %d in file '%s': %v\nRow Data: %v\n", lineNumber, inputFile, err, row)
				continue
			}
			count++

			if count%1000 == 0 {
				fmt.Printf("Processed %d records...\n", count)
			}
		}

		if err := scanner.Err(); err != nil {
			fmt.Printf("Error reading input file '%s': %v\n", inputFile, err)
		}
	}

	// Write a summary row with the total count
	countRow := []string{"Overall", "Total", "Count", "Of", "Requests", "", fmt.Sprintf("%d", count)}
	if err := writer.Write(countRow); err != nil {
		fmt.Printf("Error writing count row to CSV: %v\n", err)
	}

	fmt.Printf("Processing complete. Total records processed: %d\n", count)
}
