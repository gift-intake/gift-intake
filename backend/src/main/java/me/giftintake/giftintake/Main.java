package me.giftintake.giftintake;

import me.giftintake.giftintake.extractor.PdfExtractor;

import java.io.IOException;

public class Main {

    public static void main(String[] args) {

        // Path to the PDF file
        String pdfFilePath = "D:\\gift-intake\\charity.pdf";  // Change this path if needed

        PdfExtractor extractor = new PdfExtractor();
        try {
            // Extract text from the PDF
            String extractedText = extractor. extractTextFromPDF(pdfFilePath);

            // Print the extracted text to the console
            System.out.println("Extracted Text from PDF:");
            System.out.println(extractedText);
        } catch (IOException e) {
            e.printStackTrace();  // Print any errors if they occur
        }
    }
}

