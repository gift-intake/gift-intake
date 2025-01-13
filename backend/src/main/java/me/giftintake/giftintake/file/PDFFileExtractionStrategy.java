package me.giftintake.giftintake.file;

import java.io.File;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

@Component
public class PDFFileExtractionStrategy implements FileExtractionStrategy {

  @Override
  public @NonNull String extractText(@NonNull File file) {
    return "";
  }

}
