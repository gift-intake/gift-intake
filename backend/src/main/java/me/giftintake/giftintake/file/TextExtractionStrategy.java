package me.giftintake.giftintake.file;

import java.io.File;
import org.springframework.lang.NonNull;

public interface TextExtractionStrategy {

  /**
   * Extracts text from a file.
   *
   * @param file the file to extract text from
   * @return the extracted text
   */
  @NonNull
  String extractText(@NonNull File file);
}
