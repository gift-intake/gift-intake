package me.giftintake.giftintake.file;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Factory for creating {@link TextExtractionStrategy} instances based on the file extension.
 */
@Component
public class TextExtractionStrategyFactory {

  private final ImageTextExtractionStrategy imageFileExtractionStrategy;
  private final PDFTextExtractionStrategy pdfFileExtractionStrategy;
  private final OutlookTextExtractionStrategy outlookEmailFileExtractionStrategy;
  private final WordTextExtractionStrategy wordFileExtractionStrategy;

  @Autowired
  public TextExtractionStrategyFactory(ImageTextExtractionStrategy imageFileExtractionStrategy,
                                       PDFTextExtractionStrategy pdfFileExtractionStrategy,
                                       OutlookTextExtractionStrategy outlookEmailFileExtractionStrategy,
                                       WordTextExtractionStrategy wordFileExtractionStrategy) {
    this.imageFileExtractionStrategy = imageFileExtractionStrategy;
    this.pdfFileExtractionStrategy = pdfFileExtractionStrategy;
    this.outlookEmailFileExtractionStrategy = outlookEmailFileExtractionStrategy;
    this.wordFileExtractionStrategy = wordFileExtractionStrategy;
  }

  /**
   * Factory method for creating a {@link TextExtractionStrategy} based on the file extension.
   *
   * @param extension The file extension
   * @return The {@link TextExtractionStrategy} for the given extension
   */
  public TextExtractionStrategy getStrategy(String extension) {
    return switch (extension) {
      case ".pdf" -> this.pdfFileExtractionStrategy;
      case ".png", ".jpg" -> this.imageFileExtractionStrategy;
      case ".docx" -> this.wordFileExtractionStrategy;
      case ".msg" -> this.outlookEmailFileExtractionStrategy;
      default -> throw new IllegalArgumentException("Unsupported file type " + extension);
    };
  }
}
