package com.example.demo.machine.controller;

import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.dbQuery.service.SelectDBService;
import com.example.demo.dbQuery.service.UpdateDBService;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@RequestMapping("/api/data")
@RequiredArgsConstructor
public class MachineToDatabaseController {
    private final SelectDBService selectDBService;
    private final UpdateDBService updateDBService;

    @GetMapping("/search")
    public List<Map<String, Object>> searchData(
            @RequestParam(required = false) String eventTime) {
        return selectDBService.searchData(eventTime);
    }

    @PostMapping("/update")
    public ResponseEntity<Map<String, Object>> updateData(
        @RequestBody Map<String, Object> requestData
        ) {
            Map<String, Object> updatedData = updateDBService.updateData(requestData);
            return ResponseEntity.ok(updatedData);
    }

}
