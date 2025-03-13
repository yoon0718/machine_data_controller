// package com.example.demo.json.controller;

// import com.example.demo.dbQuery.service.InsertDBService;
// import com.example.demo.json.service.JsonDataMergeService;
// import com.fasterxml.jackson.databind.JsonNode;
// import com.fasterxml.jackson.databind.ObjectMapper;

// import lombok.RequiredArgsConstructor;
// import org.springframework.scheduling.annotation.Scheduled;
// import org.springframework.stereotype.Controller;
// import java.io.File;
// import java.io.IOException;
// import java.nio.file.Files;
// import java.nio.file.Paths;
// import java.util.ArrayList;
// import java.util.List;

// @Controller
// @RequiredArgsConstructor
// public class JsonToDatabaseController {

//     private final ObjectMapper objectMapper;
//     private final InsertDBService insertDB;
//     private final JsonDataMergeService jsonDataMergeService;
//     private final String JSON_FOLDER_PATH = "C:/Users/user/Desktop/TSITest/data_storage/upload_data/";

//     @Scheduled(fixedRate = 10000)
//     public void integrateAllJsonData(){
//         File folder = new File(JSON_FOLDER_PATH);
//         if (!folder.exists()) {
//             folder.mkdirs();
//         }
//         File[] files = folder.listFiles((dir, name) -> name.endsWith(".json"));

//         if (files == null || files.length == 0) {
//             System.out.println("JSON 파일이 없습니다.");
//             return;
//         }

//         List<JsonNode> jsonList = new ArrayList<>();

//         for (File file : files) {
//             try {
//                 String content = new String(Files.readAllBytes(Paths.get(file.getAbsolutePath())));
//                 JsonNode jsonNode = objectMapper.readTree(content);

                
//                 // insertDB.saveJsonToDatabase(jsonNode);

//                 // System.out.println("DB 저장 완료: " + file.getName());

//                 jsonList.add(jsonNode);
                
//                 // file.delete();
//             } catch (IOException e) {
//                 System.err.println("JSON 처리 중 오류 발생: " + file.getName() + " - " + e.getMessage());
//             }
//         }
        
//         // jsonDataMergeService.mergeJsonFiles(jsonList);
//     }

    
    
    
// }