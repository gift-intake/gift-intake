package me.giftintake.giftintake.file;

import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;
import java.io.File;

@Component
public class PDFFileExtractionStrategy implements FileExtractionStrategy {

    @Override
    public @NonNull String extractText(@NonNull File file) {
        return "";
    }

}
