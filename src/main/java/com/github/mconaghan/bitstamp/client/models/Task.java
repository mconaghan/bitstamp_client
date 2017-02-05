package com.github.mconaghan.bitstamp.client.models;

import com.google.common.base.MoreObjects;

import java.util.Date;
import java.util.Objects;
import java.util.Optional;

public class Task {

    private TaskId taskId;

    private String description;

    private Optional<TaskLabel> taskLabel;

    private Optional<Date> dueDate;

    private Date createdDate;

    private Date updatedDate;

    public Task(final TaskId taskIdIn, String descriptionIn) {
        this(taskIdIn, descriptionIn, Optional.empty(), Optional.empty());
    }

    public Task(final TaskId taskIdIn, String descriptionIn, final TaskLabel taskLabelIn) {
        this(taskIdIn, descriptionIn, Optional.of(taskLabelIn), Optional.empty());
    }

    public Task(final TaskId taskIdIn, String descriptionIn, final Date dueDateIn) {
        this(taskIdIn, descriptionIn, Optional.empty(), Optional.of(dueDateIn));
    }

    public Task(final TaskId taskIdIn, String descriptionIn, final TaskLabel taskLabelIn, final Date dueDateIn) {
        this(taskIdIn, descriptionIn, Optional.of(taskLabelIn), Optional.of(dueDateIn));
    }

    private Task(final TaskId taskIdIn, String descriptionIn,
                 final Optional<TaskLabel> taskLabelIn, final Optional<Date> dueDateIn) {
        taskId      = taskIdIn;
        description = descriptionIn;
        taskLabel   = taskLabelIn;
        dueDate     = dueDateIn;

        createdDate = new Date();
        updatedDate = new Date();
    }

    public TaskId getTaskId() {
        return taskId;
    }

    public String getDescription() {
        return description;
    }

    public Optional<TaskLabel> getTaskLabel() {
        return taskLabel;
    }

    public Optional<Date> getDueDate() {
        return dueDate;
    }

    public Date getUpdatedDate() {
        return updatedDate;
    }

    public void setTaskLabel(Optional<TaskLabel> taskLabel) {
        this.taskLabel = taskLabel;
    }

    public void setDueDate(Optional<Date> dueDate) {
        this.dueDate = dueDate;
    }

    public void setUpdatedDate(Date updatedDate) {
        this.updatedDate = updatedDate;
    }

    @Override
    public boolean equals(final Object obj) {
        if (obj == null) {
            return false;
        }

        if (getClass() != obj.getClass()) {
            return false;
        }

        final Task other = (Task) obj;
        return Objects.equals(taskId, other.getTaskId());
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(taskId);
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this.getClass()).add("id", taskId).add("description", description)
                .add("label", taskLabel).add("due", dueDate).add("created", createdDate).toString();
    }
}
