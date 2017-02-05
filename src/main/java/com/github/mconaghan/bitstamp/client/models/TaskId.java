package com.github.mconaghan.bitstamp.client.models;

import com.google.common.base.MoreObjects;

import java.util.Objects;

/**
 * Unique identifier for a Task.
 */
public class TaskId {

    /**
     * For now just use an internal long as the unique id.
     */
    private final long id;

    public TaskId(final long idIn) {
        id = idIn;
    }

    public long getId() {
        return id;
    }

    @Override
    public boolean equals(final Object obj) {
        if (obj == null) {
            return false;
        }

        if (getClass() != obj.getClass()) {
            return false;
        }

        final TaskId other = (TaskId) obj;
        return Objects.equals(id, other.getId());
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this.getClass()).add("id", id).toString();
    }
}
