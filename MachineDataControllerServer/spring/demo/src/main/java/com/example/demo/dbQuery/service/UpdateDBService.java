package com.example.demo.dbQuery.service;

import java.util.Map;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class UpdateDBService {
    
    private final JdbcTemplate jdbcTemplate;


    public Map<String, Object> updateData(Map<String, Object> request){
        String updateSql = "update yoontest set MESSAGE = 'TSI_Done' where (EQUIPMENTID = ? and MEASUREID = ? and MEASURETIMEKEY = ? and MEASUREITEM = ? and MEASURESITE = ? and LOTID = ? and MODULEID = ? and MODEL = ? and PARANO = ? and OPERATIONRESULT = ? and MULTIROWNAME = ? and MULTIROWVALUE = ? and INSPECTIONRESULT = ? and MEASURERESULT = ? and UPPERSPECLIMIT = ? and LOWERSPECLIMIT = ? and TARGET = ? and FACTORYID = ? and INPUTTIME = ? and OPERATIONNAME = ? and RECIPEID = ? and DATASTATE = ? and EVENT = ? and TIMEKEY = ? and EVENTTIME = ? and EVENTUSER = ? and MESSAGE = ? and EVENTCOMMENT = ?)";
        int rowsUpdated = jdbcTemplate.update(updateSql,
            request.get("EQUIPMENTID"),
            request.get("MEASUREID"),
            request.get("MEASURETIMEKEY"),
            request.get("MEASUREITEM"),
            request.get("MEASURESITE"),
            request.get("LOTID"),
            request.get("MODULEID"),
            request.get("MODEL"),
            request.get("PARANO"),
            request.get("OPERATIONRESULT"),
            request.get("MULTIROWNAME"),
            request.get("MULTIROWVALUE"),
            request.get("INSPECTIONRESULT"),
            request.get("MEASURERESULT"),
            request.get("UPPERSPECLIMIT"),
            request.get("LOWERSPECLIMIT"),
            request.get("TARGET"),
            request.get("FACTORYID"),
            request.get("INPUTTIME"),
            request.get("OPERATIONNAME"),
            request.get("RECIPEID"),
            request.get("DATASTATE"),
            request.get("EVENT"),
            request.get("TIMEKEY"),
            request.get("EVENTTIME"),
            request.get("EVENTUSER"),
            request.get("MESSAGE"),
            request.get("EVENTCOMMENT")
        );
        if (rowsUpdated == 0) {
            throw new RuntimeException("업데이트할 데이터가 없음");
        }
        

        return fetchUpdatedRow(request);
    }
    public Map<String, Object> fetchUpdatedRow(Map<String, Object> request) {
        String sql = "SELECT * FROM yoontest WHERE EQUIPMENTID = ? and MEASUREID = ? and MEASURETIMEKEY = ? and MEASUREITEM = ? and MEASURESITE = ? and LOTID = ? and MODULEID = ? and MODEL = ? and PARANO = ? and OPERATIONRESULT = ? and MULTIROWNAME = ? and MULTIROWVALUE = ? and INSPECTIONRESULT = ? and MEASURERESULT = ? and UPPERSPECLIMIT = ? and LOWERSPECLIMIT = ? and TARGET = ? and FACTORYID = ? and INPUTTIME = ? and OPERATIONNAME = ? and RECIPEID = ? and DATASTATE = ? and EVENT = ? and TIMEKEY = ? and EVENTTIME = ? and EVENTUSER = ? and EVENTCOMMENT = ?";
        return jdbcTemplate.queryForMap(sql,
        request.get("EQUIPMENTID"),
        request.get("MEASUREID"),
        request.get("MEASURETIMEKEY"),
        request.get("MEASUREITEM"),
        request.get("MEASURESITE"),
        request.get("LOTID"),
        request.get("MODULEID"),
        request.get("MODEL"),
        request.get("PARANO"),
        request.get("OPERATIONRESULT"),
        request.get("MULTIROWNAME"),
        request.get("MULTIROWVALUE"),
        request.get("INSPECTIONRESULT"),
        request.get("MEASURERESULT"),
        request.get("UPPERSPECLIMIT"),
        request.get("LOWERSPECLIMIT"),
        request.get("TARGET"),
        request.get("FACTORYID"),
        request.get("INPUTTIME"),
        request.get("OPERATIONNAME"),
        request.get("RECIPEID"),
        request.get("DATASTATE"),
        request.get("EVENT"),
        request.get("TIMEKEY"),
        request.get("EVENTTIME"),
        request.get("EVENTUSER"),
        request.get("EVENTCOMMENT")
        );
    }

}
