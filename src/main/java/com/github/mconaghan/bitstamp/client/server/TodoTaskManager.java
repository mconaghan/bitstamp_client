package com.github.mconaghan.bitstamp.client.server;

import com.github.mconaghan.bitstamp.client.models.Task;
import com.github.mconaghan.bitstamp.client.models.TaskId;
import com.github.mconaghan.bitstamp.client.models.TaskLabel;

import java.util.Collection;
import java.util.Date;
import java.util.Optional;

public interface TodoTaskManager {

    void addTask(String description, Optional<Date> dueDate, Optional<TaskLabel> label);

    Collection<Task> getAllTasks();

    Task getTask(TaskId taskId);

    Collection<Task> getTasksUnderLabel(TaskLabel taskLabel);

    Collection<Task> getTasksDueBefore(Date dueDate);

    void markTaskAsDone(TaskId taskId);

    void updateDueDateOnTask(TaskId taskId, Date dueDate);
}
