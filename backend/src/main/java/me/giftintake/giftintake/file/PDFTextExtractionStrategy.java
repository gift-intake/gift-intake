package me.giftintake.giftintake.file;

import java.io.File;
import java.io.IOException;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

/**
 * Uses the Apache PDFBox library to extract text from a PDF document.
 */
@Component
public class PDFTextExtractionStrategy implements TextExtractionStrategy {

  @Override
  public @NonNull String extractText(@NonNull File file) {
    try {
      var document = PDDocument.load(file);

      // Create a PDFTextStripper to extract text
      var pdfStripper = new PDFTextStripper();

      // Extract the text
      var text = pdfStripper.getText(document);

      // Close the document to release resources
      document.close();

      return text;
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }
}
