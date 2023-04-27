package com.example;

import com.jcraft.jsch.*;
import java.awt.AWTException;
import java.awt.Dimension;
import java.awt.Robot;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;
import javax.imageio.ImageIO;

public class App {
    private static final String REMOTE_HOST = "localhost";
    private static final String USERNAME = "username";
    private static final String PASSWORD = "password";
    private static final int PORT = 22;
    private static final String UPLOAD_DIR = "/set/your/path/here"
    private static final String ENDPOINT_URL = "http://localhost:8080";

    public static void main(String[] args) throws IOException, AWTException {
        // Get default screen device
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        // Create a new Robot object to capture the screen
        Robot robot = new Robot();
        // Capture the screen as an image
        BufferedImage image = robot.createScreenCapture(new java.awt.Rectangle(screenSize));

        // Save the captured image as a PNG file
        File file = new File("captured-image.png");
        ImageIO.write(image, "png", file);

        // Upload the captured image to the remote server using SFTP
        JSch jsch = new JSch();
        Session session = null;
        try {
            session = jsch.getSession(USERNAME, REMOTE_HOST, PORT);
            session.setConfig("StrictHostKeyChecking", "no");
            session.setPassword(PASSWORD);
            session.connect();

            Channel channel = session.openChannel("sftp");
            channel.connect();
            ChannelSftp sftpChannel = (ChannelSftp) channel;

            sftpChannel.put(new FileInputStream(file), UPLOAD_DIR + file.getName());

            sftpChannel.exit();
            session.disconnect();
        } catch (JSchException | SftpException e) {
            e.printStackTrace();
            return;
        }

        // Make a POST request to the endpoint with the uploaded file name as argument
        URL url = new URL(ENDPOINT_URL);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);

        String arg1 = file.getName();
        String jsonInputString = "{\"arg1\": \"" + arg1 + "\"}";

        try (OutputStream os = con.getOutputStream()) {
            byte[] input = jsonInputString.getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        try (BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), "utf-8"))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            System.out.println(response.toString());
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        // Delete the uploaded file
        if (file.delete()) {
            // Yippie! :) 
        } else {
            System.out.println("Failed to delete the file.");
        }
    }
}
