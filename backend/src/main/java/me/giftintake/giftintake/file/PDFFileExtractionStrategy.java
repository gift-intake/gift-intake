package me.giftintake.giftintake.file;

import java.io.File;
import java.io.IOException;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;


@Component
public class PDFFileExtractionStrategy implements FileExtractionStrategy {

  @Override
  public @NonNull String extractText(@NonNull File file) {
    try {
      PDDocument document = PDDocument.load(file);

      // Create a PDFTextStripper to extract text
      PDFTextStripper pdfStripper = new PDFTextStripper();

      // Extract the text
      String text = pdfStripper.getText(document);

      // Close the document to release resources
      document.close();

      return text;
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }
}
