package com.github.mconaghan.bitstamp.client.models;

import com.google.common.base.MoreObjects;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class TaskLabel {

    private final String label;

    private static List<TaskLabel> existingLabels = new ArrayList<>(100);

    private TaskLabel(final String labelIn) {
        label = labelIn;
    }

    @Override
    public boolean equals(final Object obj) {
        if (obj == null) {
            return false;
        }

        if (getClass() != obj.getClass()) {
            return false;
        }

        final TaskLabel taskLabel = (TaskLabel) obj;
        return Objects.equals(label, taskLabel.getLabel());
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(label);
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(label).toString();
    }
}
