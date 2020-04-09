package com.example.omr;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Base64;

public class Recognitionservice {


    public String imageToBase64(InputStream inputStream) throws Exception{
        byte[] bytes = getBytes(inputStream);
        inputStream.close();
        if (bytes == null) return null;
        String encodedString = Base64.getEncoder().encodeToString(bytes);
//        String body = String.format("{\"image\": \"%s\"}", encodedString);
//        return body.getBytes("utf-8");
        return encodedString;
    }

    private byte[] getBytes(InputStream inputStream) {
        try (ByteArrayOutputStream byteBuffer = new ByteArrayOutputStream()) {
            int bufferSize = 1024;
            byte[] buffer = new byte[bufferSize];

            int len = 0;
            while ((len = inputStream.read(buffer)) != -1) {
                byteBuffer.write(buffer, 0, len);
            }
            return byteBuffer.toByteArray();
        } catch (IOException e) {
            return null;
        }
    }
}
