package com.github.mconaghan.bitstamp.client.models;

import org.junit.Test;

import java.util.Random;

import static junit.framework.TestCase.assertFalse;
import static junit.framework.TestCase.assertTrue;
import static org.apache.commons.lang.RandomStringUtils.randomAlphanumeric;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;

public class TaskTest {

    private final Random random = new Random();

    @Test
    public void constructWithIdAndDescription() {
        long l = random.nextLong();
        String d = randomAlphanumeric(64);
        Task task = new Task(new TaskId(l), d);
        assertEquals(l, task.getTaskId().getId());
        assertEquals(d, task.getDescription());

        assertTrue(task.toString().contains(Long.toString(l)));
        assertTrue(task.toString().contains(d));
    }

    @Test
    public void constructWithIdDescriptionAndLabel() {
        long l = random.nextLong();
        String d = randomAlphanumeric(64);
        String label = randomAlphanumeric(12);
        Task task = new Task(new TaskId(l), d, new TaskLabel(label));
        assertEquals(l, task.getTaskId().getId());
        assertEquals(d, task.getDescription());
        assertEquals(label, task.getTaskLabel().toString());

        assertTrue(task.toString().contains(Long.toString(l)));
        assertTrue(task.toString().contains(d));
    }

    @Test
    public void testEquals() {
        Long l = random.nextLong();
        Long l2 = l;

        while (l == l2) {
            l2 = random.nextLong();
        }

        Task task1 = new Task(new TaskId(l), randomAlphanumeric(64));
        Task task2 = new Task(new TaskId(l), randomAlphanumeric(64));
        Task task3 = new Task(new TaskId(l2), randomAlphanumeric(64));

        assertTrue(task1.equals(task2));
        assertTrue(task2.equals(task1));

        assertFalse(task1.equals(task3));
        assertFalse(task3.equals(task2));

        assertFalse(task1.equals(null));
        assertFalse(task1.equals(new String()));
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
