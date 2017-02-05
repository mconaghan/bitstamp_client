package com.github.mconaghan.bitstamp.client.models;

import org.junit.Test;

import java.util.Random;

import static junit.framework.TestCase.assertFalse;
import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;

public class TaskIdTest {

    private final Random random = new Random();

    @Test
    public void testGetId() {
        long l = random.nextLong();
        TaskId taskId = new TaskId(l);
        assertEquals(l, taskId.getId());
    }

    @Test
    public void testToString() {
        Long l = random.nextLong();
        TaskId taskId = new TaskId(l);

        System.out.println(String.format("%s %s", taskId.toString(), Long.toString(l)));

        assertTrue(taskId.toString().contains(Long.toString(l)));
        assertTrue(taskId.toString().contains(TaskId.class.getSimpleName()));
    }

    @Test
    public void testEquals() {
        Long l = random.nextLong();
        Long l2 = l;

        while (l == l2) {
            l2 = random.nextLong();
        }

        TaskId taskId1 = new TaskId(l);
        TaskId taskId2 = new TaskId(l);
        TaskId taskId3 = new TaskId(l2);

        assertTrue(taskId1.equals(taskId2));
        assertTrue(taskId2.equals(taskId1));

        assertFalse(taskId1.equals(taskId3));
        assertFalse(taskId3.equals(taskId2));

        assertFalse(taskId1.equals(null));
        assertFalse(taskId1.equals(new String()));
    }


    @Test
    public void testHashCode() {
        Long l = random.nextLong();
        Long l2 = l;

        while (l == l2) {
            l2 = random.nextLong();
        }

        TaskId taskId1 = new TaskId(l);
        TaskId taskId2 = new TaskId(l);
        TaskId taskId3 = new TaskId(l2);

        assertEquals(taskId1.hashCode(), taskId2.hashCode());
        assertNotEquals(taskId1.hashCode(), taskId3.hashCode());
        assertNotEquals(taskId2.hashCode(), taskId3.hashCode());
    }
}
