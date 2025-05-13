package com.example.demo.json.service;
import com.fasterxml.jackson.databind.ObjectMapper;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;
import java.util.TimeZone;


@Service
@RequiredArgsConstructor
public class JsonDataStorageService {

    private final ObjectMapper objectMapper;
    private final String STORAGE_DIR = "C:/Users/user/Desktop/TSITest/data_storage/";
    

    public void saveDataAsJson(Map<String, Object> data, String ip) throws IOException {
        try{
            String EQUIPMENTID = data.get("EQUIPMENTID").toString();
            String EQUIPMENTID_DIR = STORAGE_DIR + ip + "_" + EQUIPMENTID + "/";
            
            File dir = new File(EQUIPMENTID_DIR);
            if (!dir.exists()) {
                dir.mkdirs();
            }
            
            SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd_HHmmss");
            sdf.setTimeZone(TimeZone.getDefault());
            String LOT_ID = data.get("LOTID").toString();
            String timestamp = sdf.format(new Date());
            String fileName = LOT_ID + "_" + timestamp + ".json";
            String EQUIPMENTID_filePath = EQUIPMENTID_DIR + fileName;
    
            
    
            objectMapper.writeValue(new File(EQUIPMENTID_filePath), data);
    
            System.out.println("데이터 저장 완료: " + EQUIPMENTID_filePath);
        }
        catch (Exception e) {
            System.out.println("저장 실패" );
        }
        
    }

    
}
