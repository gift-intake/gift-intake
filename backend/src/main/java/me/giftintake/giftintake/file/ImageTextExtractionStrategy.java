package me.giftintake.giftintake.file;

import java.io.File;
import net.sourceforge.tess4j.Tesseract;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

/**
 * Uses the Tesseract library to extract text from an image file.
 */
@Component
public class ImageTextExtractionStrategy implements TextExtractionStrategy {

  @Override
  public @NonNull String extractText(@NonNull File file) {
    var tesseract = new Tesseract();
    try {
      return tesseract.doOCR(file);
    } catch (Exception e) {
      throw new RuntimeException("Failed to extract text from image", e);
    }
  }

}
