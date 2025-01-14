package me.giftintake.giftintake.file;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class FileExtractionStrategyFactory {

  private final ImageFileExtractionStrategy imageFileExtractionStrategy;
  private final PDFFileExtractionStrategy pdfFileExtractionStrategy;
  private final OutlookFileExtractionStrategy outlookEmailFileExtractionStrategy;
  private final WordFileExtractionStrategy wordFileExtractionStrategy;

  @Autowired
  public FileExtractionStrategyFactory(ImageFileExtractionStrategy imageFileExtractionStrategy,
      PDFFileExtractionStrategy pdfFileExtractionStrategy,
      OutlookFileExtractionStrategy outlookEmailFileExtractionStrategy,
      WordFileExtractionStrategy wordFileExtractionStrategy) {
    this.imageFileExtractionStrategy = imageFileExtractionStrategy;
    this.pdfFileExtractionStrategy = pdfFileExtractionStrategy;
    this.outlookEmailFileExtractionStrategy = outlookEmailFileExtractionStrategy;
    this.wordFileExtractionStrategy = wordFileExtractionStrategy;
  }

  public FileExtractionStrategy getStrategy(String extension) {
    return switch (extension) {
      case ".pdf" -> this.pdfFileExtractionStrategy;
      case ".png", ".jpg" -> this.imageFileExtractionStrategy;
      case ".docx" -> this.wordFileExtractionStrategy;
      case ".msg" -> this.outlookEmailFileExtractionStrategy;
      default -> throw new IllegalArgumentException("Unsupported file type " + extension);
    };
  }
}
