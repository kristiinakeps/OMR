package com.example.omr;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Base64;

public class RecognitionService {

    public byte[] midi(String encodedString) {
        byte[] decodedBytes = Base64.getDecoder().decode(encodedString);
        return decodedBytes;
    }


    public String imageToBase64(InputStream inputStream) throws Exception{
        byte[] bytes = getBytes(inputStream);
        inputStream.close();
        if (bytes == null) return null;
        return Base64.getEncoder().encodeToString(bytes);
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
