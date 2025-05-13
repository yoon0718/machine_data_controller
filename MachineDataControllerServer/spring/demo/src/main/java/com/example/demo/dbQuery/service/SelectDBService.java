package com.example.demo.dbQuery.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class SelectDBService {
    private final JdbcTemplate jdbcTemplate;

    public List<Map<String, Object>> searchData(String eventTime){
        StringBuilder query = new StringBuilder();
        query.append("SELECT t1.* ");
        query.append("FROM yoontest t1 ");
        query.append("INNER JOIN ( ");
        query.append("    SELECT LOTID, MAX(EVENTTIME) AS max_event_time ");
        query.append("    FROM yoontest ");
        query.append("    WHERE OPERATIONNAME LIKE '%TX%' ");
        query.append("    AND OPERATIONRESULT = 'Pass' ");
        List<Object> params = new ArrayList<>();
        if (eventTime != null && !eventTime.isEmpty()) {
            query.append("    AND EVENTTIME BETWEEN ? AND ? ");
            params.add(eventTime + " 00:00:00");
            params.add(eventTime + " 23:59:59");
        }
        query.append("GROUP BY LOTID ");
        query.append(") t2 ON t1.LOTID = t2.LOTID AND t1.EVENTTIME = t2.max_event_time ");

        

        return jdbcTemplate.queryForList(query.toString(), params.toArray());
    }
    

}
