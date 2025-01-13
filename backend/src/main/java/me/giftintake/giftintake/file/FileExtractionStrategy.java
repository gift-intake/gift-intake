package me.giftintake.giftintake.file;

import org.springframework.lang.NonNull;

import java.io.File;

public interface FileExtractionStrategy {

    /**
     * Extracts text from a file.
     *
     * @param file the file to extract text from
     * @return the extracted text
     */
    @NonNull String extractText(@NonNull File file);
}
