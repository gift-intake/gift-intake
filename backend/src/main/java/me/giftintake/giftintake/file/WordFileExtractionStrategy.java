package me.giftintake.giftintake.file;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import org.apache.poi.xwpf.extractor.XWPFWordExtractor;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

@Component
public class WordFileExtractionStrategy implements FileExtractionStrategy {

  @Override
  public @NonNull String extractText(@NonNull File file) {
    try (XWPFDocument document = new XWPFDocument(new FileInputStream(file))) {
      XWPFWordExtractor extractor = new XWPFWordExtractor(document);
      return extractor.getText();
    } catch (IOException e) {
      throw new RuntimeException(e);

    }
  }

}
