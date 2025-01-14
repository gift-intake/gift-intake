package me.giftintake.giftintake.file;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import org.apache.poi.xwpf.extractor.XWPFWordExtractor;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

/**
 * Uses the Apache POI library to extract text from a Word document.
 */
@Component
public class WordTextExtractionStrategy implements TextExtractionStrategy {

  @Override
  public @NonNull String extractText(@NonNull File file) {
    try (var document = new XWPFDocument(new FileInputStream(file))) {
      var extractor = new XWPFWordExtractor(document);
      return extractor.getText();
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }
}
