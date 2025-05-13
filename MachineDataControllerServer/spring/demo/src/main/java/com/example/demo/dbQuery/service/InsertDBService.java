package com.example.demo.dbQuery.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class InsertDBService {

    private List<Map<String, Object>> batchList = new ArrayList<>();

    private final JdbcTemplate jdbcTemplate;

    public synchronized void addToBatch(Map<String, Object> data) {
        batchList.add(data);
    }

    @Async
    @Transactional
    @Scheduled(fixedRate = 5000)
    public void saveJsonToDatabase() {
        if (batchList.isEmpty()) return;

        try {
            String sql = "INSERT INTO yoontest (EQUIPMENTID, MEASUREID, MEASURETIMEKEY, MEASUREITEM, MEASURESITE, LOTID, MODULEID, MODEL, PARANO, OPERATIONRESULT, MULTIROWNAME, MULTIROWVALUE, INSPECTIONRESULT, MEASURERESULT, UPPERSPECLIMIT, LOWERSPECLIMIT, TARGET, FACTORYID, INPUTTIME, OPERATIONNAME, RECIPEID, DATASTATE, EVENT, TIMEKEY, EVENTTIME, EVENTUSER, MESSAGE, EVENTCOMMENT) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            
            List<Object[]> batchParams = new ArrayList<>();
            
            for (Map<String, Object> data : batchList) {
                batchParams.add(new Object[]{
                    data.get("EQUIPMENTID"),
                    data.get("MEASUREID"),
                    data.get("MEASURETIMEKEY"),
                    data.get("MEASUREITEM"),
                    data.get("MEASURESITE"),
                    data.get("LOTID"),
                    data.get("MODULEID"),
                    data.get("MODEL"),
                    data.get("PARANO"),
                    data.get("OPERATIONRESULT"),
                    data.get("MULTIROWNAME"),
                    data.get("MULTIROWVALUE"),
                    data.get("INSPECTIONRESULT"),
                    data.get("MEASURERESULT"),
                    data.get("UPPERSPECLIMIT"),
                    data.get("LOWERSPECLIMIT"),
                    data.get("TARGET"),
                    data.get("FACTORYID"),
                    data.get("INPUTTIME"),
                    data.get("OPERATIONNAME"),
                    data.get("RECIPEID"),
                    data.get("DATASTATE"),
                    data.get("EVENT"),
                    data.get("TIMEKEY"),
                    data.get("EVENTTIME"),
                    data.get("EVENTUSER"),
                    data.get("MESSAGE"),
                    data.get("EVENTCOMMENT")
                });
            System.out.println("DB 저장 완료: " + data.toString());
            }
            jdbcTemplate.batchUpdate(sql, batchParams);
            batchList.clear();

        }
        catch (Exception e) {
            System.err.println("DB 저장 중 오류 발생: " + e.getMessage());
        }   
        
    }
    // public void saveJsonToDatabase(Map<String, Object> data) {
    //     try {
    //         String sql = "INSERT INTO yoontest (EQUIPMENTID, MEASUREID, MEASURETIMEKEY, MEASUREITEM, MEASURESITE, LOTID, MODULEID, MODEL, PARANO, OPERATIONRESULT, MULTIROWNAME, MULTIROWVALUE, INSPECTIONRESULT, MEASURERESULT, UPPERSPECLIMIT, LOWERSPECLIMIT, TARGET, FACTORYID, INPUTTIME, OPERATIONNAME, RECIPEID, DATASTATE, EVENT, TIMEKEY, EVENTTIME, EVENTUSER, MESSAGE, EVENTCOMMENT) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
    //         jdbcTemplate.update(sql,
    //             data.get("EQUIPMENTID"),
    //             data.get("MEASUREID"),
    //             data.get("MEASURETIMEKEY"),
    //             data.get("MEASUREITEM"),
    //             data.get("MEASURESITE"),
    //             data.get("LOTID"),
    //             data.get("MODULEID"),
    //             data.get("MODEL"),
    //             data.get("PARANO"),
    //             data.get("OPERATIONRESULT"),
    //             data.get("MULTIROWNAME"),
    //             data.get("MULTIROWVALUE"),
    //             data.get("INSPECTIONRESULT"),
    //             data.get("MEASURERESULT"),
    //             data.get("UPPERSPECLIMIT"),
    //             data.get("LOWERSPECLIMIT"),
    //             data.get("TARGET"),
    //             data.get("FACTORYID"),
    //             data.get("INPUTTIME"),
    //             data.get("OPERATIONNAME"),
    //             data.get("RECIPEID"),
    //             data.get("DATASTATE"),
    //             data.get("EVENT"),
    //             data.get("TIMEKEY"),
    //             data.get("EVENTTIME"),
    //             data.get("EVENTUSER"),
    //             data.get("MESSAGE"),
    //             data.get("EVENTCOMMENT")
    //     );

    //     System.out.println("DB 저장 완료: " + data.toString());
    //     } catch (Exception e) {
    //         System.err.println("DB 저장 중 오류 발생: " + e.getMessage());
    //     }
        
    // }
    // public void saveJsonToDatabase(JsonNode jsonNode) {
    //     try {
    //         String sql = "INSERT INTO yoontest (EQUIPMENTID, MEASUREID, MEASURETIMEKEY, MEASUREITEM, MEASURESITE, LOTID, MODULEID, MODEL, PARANO, OPERATIONRESULT, MULTIROWNAME, MULTIROWVALUE, INSPECTIONRESULT, MEASURERESULT, UPPERSPECLIMIT, LOWERSPECLIMIT, TARGET, FACTORYID, INPUTTIME, OPERATIONNAME, RECIPEID, DATASTATE, EVENT, TIMEKEY, EVENTTIME, EVENTUSER, MESSAGE, EVENTCOMMENT) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
    //         jdbcTemplate.update(sql,
    //             data.get("EQUIPMENTID"),
    //             data.get("MEASUREID"),
    //             data.get("MEASURETIMEKEY"),
    //             data.get("MEASUREITEM"),
    //             data.get("MEASURESITE"),
    //             data.get("LOTID"),
    //             data.get("MODULEID"),
    //             data.get("MODEL"),
    //             data.get("PARANO"),
    //             data.get("OPERATIONRESULT"),
    //             data.get("MULTIROWNAME"),
    //             data.get("MULTIROWVALUE"),
    //             data.get("INSPECTIONRESULT"),
    //             data.get("MEASURERESULT"),
    //             data.get("UPPERSPECLIMIT"),
    //             data.get("LOWERSPECLIMIT"),
    //             data.get("TARGET"),
    //             data.get("FACTORYID"),
    //             data.get("INPUTTIME"),
    //             data.get("OPERATIONNAME"),
    //             data.get("RECIPEID"),
    //             data.get("DATASTATE"),
    //             data.get("EVENT"),
    //             data.get("TIMEKEY"),
    //             data.get("EVENTTIME"),
    //             data.get("EVENTUSER"),
    //             data.get("MESSAGE"),
    //             data.get("EVENTCOMMENT").asText()
    //     );

    //     System.out.println("DB 저장 완료: " + data.toString());
    //     } catch (Exception e) {
    //         System.err.println("DB 저장 중 오류 발생: " + e.getMessage());
    //     }
        
    // }
    
}
