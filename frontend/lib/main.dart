import 'dart:html' as html; // Only for web
import 'dart:io'; // Only for mobile (Android/iOS)
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  // Ensure that the app waits for the environment variables to load
  await dotenv.load();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter File Upload',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: FileUploadScreen(),
    );
  }
}

class FileUploadScreen extends StatefulWidget {
  @override
  _FileUploadScreenState createState() => _FileUploadScreenState();
}

class _FileUploadScreenState extends State<FileUploadScreen> {
  String _responseMessage = '';

  // Method to pick a file and upload it
  Future<void> uploadFile() async {
    // Open file picker
    FilePickerResult? result = await FilePicker.platform.pickFiles();
    String apiUrl = dotenv.env['BACKEND_URL'] ?? 'https://default-api-url.com';

    if (result != null) {
      // Get the selected file
      PlatformFile file = result.files.first;

      // Check if the platform is web
      if (html.window.navigator.userAgent.contains('Chrome')) {
        // For web: use bytes property (because `path` is null on web)
        final bytes = file.bytes;

        if (bytes != null) {
          // Prepare multipart request for web
          var request = http.MultipartRequest(
              'POST', Uri.parse("$apiUrl/upload"));

          // Add the file to the request as a byte stream
          request.files.add(http.MultipartFile.fromBytes(
            'file', 
            bytes, 
            filename: file.name, 
            contentType: MediaType('application', 'octet-stream'),
          ));

          // Send the request and handle the response
          var response = await request.send();

          if (response.statusCode == 200) {
            setState(() {
              _responseMessage = "File uploaded successfully!";
            });
          } else {
            setState(() {
              _responseMessage = "File upload failed with status code: ${response.statusCode}";
            });
          }
        }
      } else {
        // For mobile: use the path property to get the file's path
        File fileToUpload = File(file.path!);

        var request = http.MultipartRequest(
            'POST', Uri.parse('https://your-fastapi-app-name.herokuapp.com/upload_file'));

        request.files.add(await http.MultipartFile.fromPath(
          'file',
          fileToUpload.path,
          contentType: MediaType('application', 'octet-stream'),
        ));

        var response = await request.send();

        if (response.statusCode == 200) {
          setState(() {
            _responseMessage = "File uploaded successfully!";
          });
        } else {
          setState(() {
            _responseMessage = "File upload failed with status code: ${response.statusCode}";
          });
        }
      }
    } else {
      // No file selected
      setState(() {
        _responseMessage = "No file selected.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('File Upload Example'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              ElevatedButton(
                onPressed: () async {
                  await uploadFile();
                },
                child: Text('Upload File'),
              ),
              SizedBox(height: 20),
              Text(
                _responseMessage,
                style: TextStyle(fontSize: 18, color: Colors.blue),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
