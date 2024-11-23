import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;

void main() async {
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
    const String backendUrl = "https://onboarding-agent-f2d8f7faa9f8.herokuapp.com";

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
            setState(() {
              _responseMessage = "File uploaded successfully! Data: ${response.stream.toString()}";
            });
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