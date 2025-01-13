package me.giftintake.giftintake.file;

import java.io.File;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class FileExtractionStrategyFactory {

  private final ImageFileExtractionStrategy imageFileExtractionStrategy;
  private final PDFFileExtractionStrategy pdfFileExtractionStrategy;

  @Autowired
  public FileExtractionStrategyFactory(ImageFileExtractionStrategy imageFileExtractionStrategy,
      PDFFileExtractionStrategy pdfFileExtractionStrategy) {
    this.imageFileExtractionStrategy = imageFileExtractionStrategy;
    this.pdfFileExtractionStrategy = pdfFileExtractionStrategy;
  }

  public FileExtractionStrategy getStrategy(File file) {
    String fileName = file.getName();
    if (fileName.contains(".pdf")) {
      return this.pdfFileExtractionStrategy;
    } else if (fileName.contains(".png") || fileName.contains(".jpg")) {
      return this.imageFileExtractionStrategy;
    } else if (fileName.contains(".docx")) {
      throw new UnsupportedOperationException("Word documents are not currently supported");
    } else {
      throw new IllegalArgumentException("Unsupported file type");
    }
  }
}
