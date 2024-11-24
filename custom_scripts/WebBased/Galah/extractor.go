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
	outputDir := flag.String("output", "output/", "Directory for output CSV files")
	flag.Parse()

	inputFiles := []string{
		"./Galah/AzureGalah_export.json",
		"./Galah/GoogleGalah_export.json",
		"./Galah/OracleGalah_export.json",
		"./Galah/DigitalOceanGalah_export.json",
	}

	if err := os.MkdirAll(*outputDir, os.ModePerm); err != nil {
		fmt.Printf("Error creating output directory '%s': %v\n", *outputDir, err)
		return
	}

	for _, inputFile := range inputFiles {
		file, err := os.Open(inputFile)
		if err != nil {
			fmt.Printf("Error opening input file '%s': %v\n", inputFile, err)
			continue
		}
		defer file.Close()

		outputFileName := filepath.Join(*outputDir, filepath.Base(inputFile)+".csv")
		outputFile, err := os.Create(outputFileName)
		if err != nil {
			fmt.Printf("Error creating output file '%s': %v\n", outputFileName, err)
			return
		}
		defer outputFile.Close()

		writer := csv.NewWriter(outputFile)
		defer writer.Flush()

		header := []string{"EventTime", "SrcIP", "HasError", "Request Body", "Method", "Request Path", "Response Body"}
		if err := writer.Write(header); err != nil {
			fmt.Printf("Error writing header to CSV: %v\n", err)
			return
		}

		scanner := bufio.NewScanner(file)
		lineNumber := 0
		count := 0

		for scanner.Scan() {
			lineNumber++
			line := scanner.Text()
			var entry LogEntry

			if err := json.Unmarshal([]byte(line), &entry); err != nil {
				fmt.Printf("Error parsing JSON on line %d in file '%s': %v\nLine Content: %s\n", lineNumber, inputFile, err, line)
				continue
			}

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
				fmt.Printf("Processed %d records for file '%s'...\n", count, inputFile)
			}
		}

		if err := scanner.Err(); err != nil {
			fmt.Printf("Error reading input file '%s': %v\n", inputFile, err)
		}

		fmt.Printf("Finished processing file '%s'. Total records: %d\n", inputFile, count)
	}
}
