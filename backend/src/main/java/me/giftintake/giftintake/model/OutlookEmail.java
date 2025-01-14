package me.giftintake.giftintake.model;

import java.util.List;

public record OutlookEmail(String body, List<Attachment> attachments) {

  public record Attachment(String name, String extension, String content) {

  }
}
