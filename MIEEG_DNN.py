# %cd 'Write the data directory'
import numpy as np
import scipy.io
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.layers import Input, Dense, Dropout, BatchNormalization, Activation
from keras.models import Model
from keras.utils import to_categorical
import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    data = scipy.io.loadmat(file_path)
    x_train, x_test, y_train, y_test = data['x_train'], data['x_test'], data['y_train'], data['y_test']
    return x_train, x_test, y_train, y_test

def preprocess_data(x_train, x_test):
    # Flatten the time samples for each trial while keeping the channel information
    num_trials_train, num_time_samples, num_channels = x_train.shape
    num_trials_test, _, _ = x_test.shape

    x_train_reshaped = x_train.reshape((num_trials_train, -1))
    x_test_reshaped = x_test.reshape((num_trials_test, -1))

    # Apply StandardScaler
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train_reshaped)
    x_test_scaled = scaler.transform(x_test_reshaped)

    # Reshape back to the original shape
    x_train_scaled = x_train_scaled.reshape((num_trials_train, num_time_samples, num_channels))
    x_test_scaled = x_test_scaled.reshape((num_trials_test, num_time_samples, num_channels))

    return x_train_scaled, x_test_scaled

def create_model(input_shape, layer_sizes, activations, dropout_rates):
    assert len(layer_sizes) == len(activations) == len(dropout_rates), "Sizes of layer_sizes, activations, and dropout_rates must be the same."

    inputs = Input(shape=input_shape)
    x = inputs

    for size, activation, dropout_rate in zip(layer_sizes, activations, dropout_rates):
        x = Dense(size, activation=None)(x)
        x = BatchNormalization()(x)
        x = Activation(activation)(x)
        x = Dropout(dropout_rate)(x)

    outputs = Dense(2, activation='softmax')(x)  # Assuming 2 output classes (binary classification)

    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model

def train_model(model, x_train, y_train, epochs=10, batch_size=32):
    y_train_categorical = to_categorical(y_train, num_classes=2)  # assuming binary classification
    history = model.fit(x_train, y_train_categorical, epochs=epochs, batch_size=batch_size, validation_split=0.2)
    return history

def evaluate_model(model, x_test, y_test):
    y_test_categorical = to_categorical(y_test, num_classes=2)  # assuming binary classification
    loss, accuracy = model.evaluate(x_test, y_test_categorical)
    print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")
    return loss, accuracy

def plot_history(history):
    plt.figure(figsize=(12, 6))

    # Plot training and validation accuracies
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()

    # Plot training and validation losses
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main(subject_id, run_for_all_subjects=True, output_dir="."):
    results = []

    if run_for_all_subjects:
        subject_range = range(1, 10)
    else:
        subject_range = [subject_id]

    for subject_id in subject_range:
        file_path = f'sub{subject_id}.mat'
        x_train, x_test, y_train, y_test = load_data(file_path)
        x_train, x_test = preprocess_data(x_train, x_test)
        num_trials, num_time_samples, num_channels = x_train.shape
        x_train = x_train.reshape((num_trials, -1))
        input_shape = x_train.shape[1:]

        num_trials, num_time_samples, num_channels = x_test.shape
        x_test = x_test.reshape((num_trials, -1))

        # Choose Hyperparameters
        layer_sizes = [128, 64]
        activations = ['relu', 'relu']
        dropout_rates = [0.5, 0.5]
        epochs = 30
        batch_size = 16

        model = create_model(input_shape, layer_sizes, activations, dropout_rates)
        history = train_model(model, x_train, y_train, epochs=epochs, batch_size=batch_size)

        loss, accuracy = evaluate_model(model, x_test, y_test)
        results.append({
            'Subject': subject_id,
            'Train Loss': history.history['loss'][-1],
            'Test Loss': loss,
            'Train Acc': history.history['accuracy'][-1],
            'Test Acc': accuracy
        })

        plot_history(history)

    # Save results to Excel
    output_file = os.path.join(output_dir, f'results.xlsx')
    results_df = pd.DataFrame(results)
    # Calculate the mean of each column and append as a new row
    mean_row = results_df.mean(axis=0)
    results_df = results_df.append(mean_row, ignore_index=True)
    results_df.iloc[-1, 0] = 'Mean'
    results_df.to_excel(output_file, index=False)

    mean_accuracy_train = results_df['Train Accuracy'].mean()
    mean_accuracy_test = results_df['Test Accuracy'].mean()

    print(f"\nMean Accuracy across all subjects (Train): {mean_accuracy_train:.4f}")
    print(f"Mean Accuracy across all subjects (Test): {mean_accuracy_test:.4f}")

if __name__ == "__main__":
    main(subject_id=1, run_for_all_subjects=True, output_dir="Write the directory you want to save the results")