package me.giftintake.giftintake.model;

import java.nio.file.Path;
import java.util.List;

public record OutlookEmail(String body, List<Path> attachments) {

}
