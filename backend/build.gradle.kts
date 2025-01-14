plugins {
	java
	id("org.springframework.boot") version "3.4.1"
	id("io.spring.dependency-management") version "1.1.7"
}

group = "me.giftintake"
version = "0.0.1-SNAPSHOT"

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(17)
	}
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-mail")
	implementation("org.springframework.boot:spring-boot-starter-web")
    implementation ("org.apache.pdfbox:pdfbox:2.0.32")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
	implementation("org.apache.poi:poi:5.4.0")
	implementation("org.apache.poi:poi-scratchpad:5.4.0")
    implementation("org.apache.poi:poi-ooxml:5.4.0")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
	implementation("net.sourceforge.tess4j:tess4j:5.13.0")
}

tasks.withType<Test> {
	useJUnitPlatform()
}
