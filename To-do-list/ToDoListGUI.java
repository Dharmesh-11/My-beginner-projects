import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Set;

public class ToDoListGUI {
    private JFrame frame;
    private DefaultListModel<Task> taskListModel;
    private JList<Task> taskList;
    private JTextField taskInput;
    private ArrayList<Task> tasks = new ArrayList<>();
    private boolean darkMode = false;

    private JPanel buttonPanel;
    private JButton toggleModeButton;

    private JButton addButton, completeButton, deleteButton, resetButton, generateButton;

    private int streak = 0;
    private JLabel streakLabel;
    private JProgressBar progressBar;  // 📊 Progress bar

    private String[] quotes = {
        "You're crushing it!",
        "One step closer to glory!",
        "Keep the momentum going!",
        "You're unstoppable!",
        "Every task done is a win!"
    };

    private String[] generatedTasks = {
        "Drink a glass of water",
        "Do 10 pushups",
        "Plan world domination ",
        "Text a friend you miss them",
        "Write one sentence in your journal ",
        "Stare at the ceiling and reflect ",
        "Clean your desk ",
        "Buy snacks",
        "Practice deep breathing",
        "Invent a new dance move",
        "Write a letter to your future self.",
        "Organize your workspace for 10 minutes",
        "Take a 5-minute walk outside and get some fresh air",
        "Learn a new word in a different language",
        "Plan your meals for the week",
        "Try a new recipe and cook something you’ve never made before",
        "Do 20 pushups or sit-ups",
        "Clean your phone screen and organize your apps",
        "Call or message a friend you haven’t talked to in a while",
        "Spend 10 minutes practicing mindfulness or meditation.",
        "Write a quick gratitude list of 5 things you’re thankful for",
        "Read a chapter of a book or an article on something interesting",
        "Set a small goal for tomorrow and write it down",
        "Do a random act of kindness for someone today",
        "Plan a short weekend getaway or day trip."
    };

    private Color lightBackground = new Color(240, 248, 255);
    private Color darkBackground = new Color(30, 30, 30);

    private Color lightInput = Color.WHITE;
    private Color darkInput = new Color(50, 50, 50);

    private Color lightText = Color.BLACK;
    private Color darkText = Color.WHITE;

    private Font font = new Font("Segoe UI", Font.PLAIN, 16);

    private Timer timer;
    private SimpleDateFormat timeFormat;

    public ToDoListGUI() {
        frame = new JFrame("AI Task Generator + Theme To-Do List");
        frame.setSize(500, 650);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        taskInput = new JTextField();
        taskInput.setFont(font);
        taskInput.setBorder(BorderFactory.createLineBorder(Color.GRAY, 2));
        taskInput.setPreferredSize(new Dimension(450, 40));

        taskListModel = new DefaultListModel<>();
        taskList = new JList<>(taskListModel);
        taskList.setFont(font);
        taskList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        taskList.setFixedCellHeight(40);
        taskList.setBackground(lightBackground);
        taskList.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        taskList.setCellRenderer(new TaskCellRenderer(this));
        JScrollPane scrollPane = new JScrollPane(taskList);

        addButton = createStyledButton("Add Task");
        completeButton = createStyledButton("Mark as Complete");
        deleteButton = createStyledButton("Delete Task");
        resetButton = createStyledButton("Reset");
        toggleModeButton = createStyledButton("Dark Mode");
        generateButton = createStyledButton("Generate Tasks");

        buttonPanel = new JPanel(new GridLayout(5, 2, 10, 10));
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        streakLabel = new JLabel("Streak: 0 | Time: 00:00:00");
        streakLabel.setFont(font);

        progressBar = new JProgressBar(0, 100);  // 📊 Initialize progress bar
        progressBar.setStringPainted(true);
        progressBar.setFont(font);
        progressBar.setForeground(new Color(50, 205, 50));  // Lime green
        progressBar.setPreferredSize(new Dimension(400, 30));

        buttonPanel.add(addButton);
        buttonPanel.add(completeButton);
        buttonPanel.add(deleteButton);
        buttonPanel.add(resetButton);
        buttonPanel.add(toggleModeButton);
        buttonPanel.add(generateButton);
        buttonPanel.add(streakLabel);

        JPanel bottomPanel = new JPanel(new BorderLayout()); // Wrap buttons + progress
        bottomPanel.add(buttonPanel, BorderLayout.CENTER);
        bottomPanel.add(progressBar, BorderLayout.SOUTH);

        frame.add(taskInput, BorderLayout.NORTH);
        frame.add(scrollPane, BorderLayout.CENTER);
        frame.add(bottomPanel, BorderLayout.SOUTH);

        addButton.addActionListener(e -> {
            String description = taskInput.getText().trim();
            if (!description.isEmpty()) {
                Task task = new Task(description);
                taskListModel.addElement(task);
                tasks.add(task);
                taskInput.setText("");

                if (description.equalsIgnoreCase("cat")) {
                    JOptionPane.showMessageDialog(frame,
                            "Meow! You've summoned the cat overlord!",
                            "Easter Egg!",
                            JOptionPane.PLAIN_MESSAGE);
                }

                updateProgressBar();
            }
        });

        completeButton.addActionListener(e -> {
            int index = taskList.getSelectedIndex();
            if (index != -1) {
                Task task = taskListModel.getElementAt(index);
                if (!task.isCompleted()) {
                    task.setCompleted(true);
                    streak++;
                    streakLabel.setText("Streak: " + streak + " | Time: " + getCurrentTime());
                    JOptionPane.showMessageDialog(frame,
                            quotes[(int) (Math.random() * quotes.length)],
                            "Motivation Boost!",
                            JOptionPane.INFORMATION_MESSAGE);
                }
                taskList.repaint();
                updateProgressBar();
            }
        });

        deleteButton.addActionListener(e -> {
            int index = taskList.getSelectedIndex();
            if (index != -1) {
                taskListModel.remove(index);
                tasks.remove(index);
                updateProgressBar();
            }
        });

        resetButton.addActionListener(e -> {
            taskListModel.clear();
            tasks.clear();
            streak = 0;
            streakLabel.setText("Streak: 0 | Time: " + getCurrentTime());
            updateProgressBar();
        });

        toggleModeButton.addActionListener(e -> {
            darkMode = !darkMode;
            updateTheme();
        });

        generateButton.addActionListener(e -> {
            int numTasks = 5 + (int) (Math.random() * 3);
            for (int i = 0; i < numTasks; i++) {
                String taskText = generatedTasks[(int) (Math.random() * generatedTasks.length)];
                Task task = new Task(taskText);
                taskListModel.addElement(task);
                tasks.add(task);
            }
            JOptionPane.showMessageDialog(frame,
                    "Here's your productivity blast!",
                    "Tasks Generated",
                    JOptionPane.INFORMATION_MESSAGE);
            updateProgressBar();
        });

        startTimer();
        updateTheme();
        frame.setVisible(true);
    }

    private void updateTheme() {
        Color bg = darkMode ? darkBackground : lightBackground;
        Color fg = darkMode ? darkText : lightText;
        Color inputBg = darkMode ? darkInput : lightInput;

        frame.getContentPane().setBackground(bg);
        buttonPanel.setBackground(bg);
        taskInput.setBackground(inputBg);
        taskInput.setForeground(fg);
        taskInput.setCaretColor(fg);
        streakLabel.setForeground(fg);
        taskList.setBackground(darkMode ? new Color(50, 50, 50) : lightBackground);
        taskList.setForeground(fg);
        taskList.setSelectionBackground(darkMode ? new Color(70, 130, 180) : new Color(173, 216, 230));

        if (darkMode) {
            addButton.setBackground(new Color(70, 130, 180));
            completeButton.setBackground(new Color(60, 179, 113));
            deleteButton.setBackground(new Color(220, 20, 60));
            resetButton.setBackground(new Color(218, 165, 32));
            toggleModeButton.setBackground(new Color(100, 100, 100));
            generateButton.setBackground(new Color(123, 104, 238));
        } else {
            addButton.setBackground(new Color(100, 149, 237));
            completeButton.setBackground(new Color(144, 238, 144));
            deleteButton.setBackground(new Color(255, 99, 71));
            resetButton.setBackground(new Color(255, 215, 0));
            toggleModeButton.setBackground(new Color(105, 105, 105));
            generateButton.setBackground(new Color(186, 85, 211));
        }

        JButton[] buttons = { addButton, completeButton, deleteButton, resetButton, toggleModeButton, generateButton };
        for (JButton b : buttons) {
            b.setForeground(Color.WHITE);
        }

        toggleModeButton.setText(darkMode ? "Light Mode" : "Dark Mode");
    }

    private JButton createStyledButton(String text) {
        JButton button = new JButton(text);
        button.setFont(font);
        button.setFocusPainted(false);
        button.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        return button;
    }

    private void startTimer() {
        timer = new Timer();
        timeFormat = new SimpleDateFormat("HH:mm:ss");

        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                SwingUtilities.invokeLater(() -> streakLabel.setText("Streak: " + streak + " | Time: " + getCurrentTime()));
            }
        }, 0, 1000);
    }

    private String getCurrentTime() {
        return timeFormat.format(new Date());
    }

    // 📊 Progress Bar Helper
    private void updateProgressBar() {
        int total = taskListModel.size();
        if (total == 0) {
            progressBar.setValue(0);
            progressBar.setString("No tasks yet");
            return;
        }

        int completed = 0;
        for (int i = 0; i < total; i++) {
            if (taskListModel.getElementAt(i).isCompleted()) {
                completed++;
            }
        }

        int percent = (int) ((completed / (double) total) * 100);
        progressBar.setValue(percent);
        progressBar.setString("Completed: " + completed + "/" + total);
    }

    private static class TaskCellRenderer extends DefaultListCellRenderer {
        private ToDoListGUI gui;

        public TaskCellRenderer(ToDoListGUI gui) {
            this.gui = gui;
        }

        @Override
        public Component getListCellRendererComponent(JList<?> list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
            super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
            Task task = (Task) value;
            setText(task.toString());

            Color textColor = task.isCompleted()
                    ? (gui.darkMode ? Color.LIGHT_GRAY : Color.DARK_GRAY)
                    : (gui.darkMode ? Color.WHITE : Color.BLACK);

            setForeground(textColor);

            if (gui.darkMode) {
                setBackground(index % 2 == 0 ? new Color(45, 45, 45) : new Color(60, 60, 60));
            } else {
                setBackground(new Color(255, 255, 255));
            }

            if (isSelected) {
                setBackground(new Color(70, 130, 180));
                setForeground(Color.WHITE);
            }

            return this;
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(ToDoListGUI::new);
    }
}

// Add this simple Task class if not already present
class Task {
    private String description;
    private boolean completed = false;

    public Task(String description) {
        this.description = description;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean value) {
        completed = value;
    }

    @Override
    public String toString() {
        return completed ? "[✔] " + description : "[ ] " + description;
    }

    public String getDescription() {// TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getDescription'");
    }
}
