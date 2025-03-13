// package com.example.demo.json.service;

// import java.io.File;
// import java.io.IOException;
// import java.text.SimpleDateFormat;
// import java.util.Date;
// import java.util.List;
// import java.util.TimeZone;

// import org.springframework.stereotype.Service;

// import com.fasterxml.jackson.databind.JsonNode;
// import com.fasterxml.jackson.databind.ObjectMapper;
// import com.fasterxml.jackson.databind.node.ArrayNode;
// import com.fasterxml.jackson.databind.node.ObjectNode;

// import lombok.RequiredArgsConstructor;

// @Service
// @RequiredArgsConstructor
// public class JsonDataMergeService {

// private final ObjectMapper objectMapper;
// private final String MERGED_JSON_PATH = "C:/Users/user/Desktop/TSITest/integrateAllJsonData/";

//     public void mergeJsonFiles(List<JsonNode> jsonList) {
//         if (jsonList == null || jsonList.isEmpty()) {
//             System.err.println("병합할 JSON 데이터가 없습니다.");
//             return;
//         }

//         try {
//             ArrayNode mergedArray = objectMapper.createArrayNode();
//             for (JsonNode node : jsonList) {
//                 mergedArray.add(node);
//             }

            
//             SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd_HHmmss");
//             sdf.setTimeZone(TimeZone.getDefault());
//             String timestamp = sdf.format(new Date());

//             File dir = new File(MERGED_JSON_PATH);
//             if(!dir.exists()){
//                 dir.mkdirs();
//             }
//             String MERGED_JSON = MERGED_JSON_PATH + timestamp + ".json";
            
//             File mergedFile = new File(MERGED_JSON);
            

            
//             ObjectNode root = objectMapper.createObjectNode();
//             root.set(timestamp, mergedArray);

            
//             objectMapper.writerWithDefaultPrettyPrinter().writeValue(mergedFile, mergedArray);
//             System.out.println("JSON 파일 병합 완료: " + mergedFile.getAbsolutePath());

//         } catch (IOException e) {
//             System.err.println("JSON 병합 오류: " + e.getMessage());
//         }
//     }
// }
