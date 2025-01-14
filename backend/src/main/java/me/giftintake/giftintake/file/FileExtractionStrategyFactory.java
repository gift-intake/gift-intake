package me.giftintake.giftintake.file;

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

  public FileExtractionStrategy getStrategy(String extension) {
    if (extension.equals(".pdf")) {
      return this.pdfFileExtractionStrategy;
    } else if (extension.equals(".png") || extension.equals(".jpg")) {
      return this.imageFileExtractionStrategy;
    } else if (extension.equals(".docx")) {
      throw new UnsupportedOperationException("Word documents are not currently supported");
    } else {
      throw new IllegalArgumentException("Unsupported file type");
    }
  }
}
