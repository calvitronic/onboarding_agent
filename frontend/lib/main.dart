// Only for mobile platforms
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  const environment = String.fromEnvironment('ENVIRONMENT', defaultValue: 'development');

  // Load the appropriate .env file
  if (environment == 'production') {
    await dotenv.load(fileName: ".env.prod");
  } else {
    await dotenv.load(fileName: ".env.dev");
  }
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'File Upload Example',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const FileUploadScreen(),
    );
  }
}

class FileUploadScreen extends StatefulWidget {
  const FileUploadScreen({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _FileUploadScreenState createState() => _FileUploadScreenState();
}

class _FileUploadScreenState extends State<FileUploadScreen> {
  String _responseMessage = '';

  Future<void> uploadFile() async {
    // Let user pick a file
    FilePickerResult? result = await FilePicker.platform.pickFiles(type: FileType.custom, allowedExtensions: ["csv", "xlsx", "xls", "pdf", "docx", "json"]);
    final String backendUrl = dotenv.env['BACKEND_URL'] ?? 'Unknown';

    if (result != null) {
      // Get the selected file
      PlatformFile file = result.files.first;

      // For web, use bytes property (path is not available)
      final bytes = file.bytes;
      if (bytes != null) {
        try {
          var request = http.MultipartRequest('POST', Uri.parse("$backendUrl/upload"));
          request.files.add(http.MultipartFile.fromBytes('file', bytes, filename: file.name));

          var response = await request.send();

          if (response.statusCode == 200) {
            // Parse the response body
            String responseBody = await response.stream.bytesToString();
            var responseData = jsonDecode(responseBody); // Decode JSON

            // Extract the validated data
            if (responseData['status'] == 'success') {
              var validatedData = responseData['validated_data'];

              setState(() {
                _responseMessage = "File uploaded successfully!\n\nValidated Data:\n$validatedData";
              });
            } else {
              setState(() {
                _responseMessage = "Upload failed: ${responseData['message']}";
              });
            }
          } else {
            setState(() {
              _responseMessage = "Upload failed: ${response.statusCode}";
            });
          }
        } catch (e) {
          setState(() {
            _responseMessage = "An error occurred: $e";
          });
        }
      } else {
        setState(() {
          _responseMessage = "No file selected.";
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('File Upload Example')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: uploadFile,
              child: const Text('Upload File'),
            ),
            const SizedBox(height: 20),
            Text(
              _responseMessage,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16, color: Colors.black),
            ),
          ],
        ),
      ),
    );
  }
}