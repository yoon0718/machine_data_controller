package com.example.demo.json.controller;

import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.bind.annotation.*;

import com.example.demo.dbQuery.service.InsertDBService;
import com.example.demo.json.service.JsonDataStorageService;

import java.util.Map;


@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
@EnableAsync
public class DataReceiverController {

    private final JsonDataStorageService jsonDataStorageService;
    private final InsertDBService insertDBService;

    @PostMapping("/receive")
    public ResponseEntity<String> receiveData(@RequestBody Map<String, Object> data, HttpServletRequest request) {
        try {
            String clientIp = request.getRemoteAddr();
            jsonDataStorageService.saveDataAsJson(data, clientIp);
            insertDBService.addToBatch(data);
            return ResponseEntity.ok("데이터가 JSON 파일로 저장되었습니다.");
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("저장 실패: " + e.getMessage());
        }
    }
    

    
}
