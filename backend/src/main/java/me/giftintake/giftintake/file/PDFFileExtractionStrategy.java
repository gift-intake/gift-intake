package me.giftintake.giftintake.file;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.IOException;


public class PDFFileExtractionStrategy implements FileExtractionStrategy {

  public static String extractTextFromPDF(String filePath) throws IOException {
        // Load the PDF document
        PDDocument document = PDDocument.load(new File(filePath));

        // Create a PDFTextStripper to extract text
        PDFTextStripper pdfStripper = new PDFTextStripper();

        // Extract the text
        String text = pdfStripper.getText(document);

        // Close the document to release resources
        document.close();

        return text;
    }

}
