import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from io import StringIO

from app.calculator_repl import calculator_repl
from app.exceptions import ValidationError, OperationError


class TestCalculatorREPL:
    """Test suite for calculator REPL functionality."""

    @patch('builtins.input', side_effect=['help', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout, mock_input):
        """Test that help command displays available commands."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Available commands:" in output
        assert "add, subtract, multiply, divide" in output
        assert "history" in output
        assert "exit" in output

    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_exit_command(self, mock_stdout, mock_input):
        """Test that exit command terminates the REPL."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Goodbye!" in output

    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_exit_with_save_error(self, mock_stdout, mock_input):
        """Test exit command handles save errors gracefully."""
        with patch('app.calculator.Calculator.save_history', side_effect=Exception("Save failed")):
            calculator_repl()
            output = mock_stdout.getvalue()
            assert "Warning: Could not save history" in output

    @patch('builtins.input', side_effect=['history', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_history_command_empty(self, mock_stdout, mock_input):
        """Test history command with no calculations."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "No calculations in history" in output

    @patch('builtins.input', side_effect=['add', '5', '3', 'history', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_history_command_with_entries(self, mock_stdout, mock_input):
        """Test history command displays calculations."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Calculation History:" in output
        assert "1." in output

    @patch('builtins.input', side_effect=['clear', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_clear_command(self, mock_stdout, mock_input):
        """Test clear command clears history."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "History cleared" in output

    @patch('builtins.input', side_effect=['undo', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_undo_command_empty(self, mock_stdout, mock_input):
        """Test undo with nothing to undo."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Nothing to undo" in output

    @patch('builtins.input', side_effect=['add', '5', '3', 'undo', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_undo_command_success(self, mock_stdout, mock_input):
        """Test successful undo operation."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Operation undone" in output

    @patch('builtins.input', side_effect=['redo', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_redo_command_empty(self, mock_stdout, mock_input):
        """Test redo with nothing to redo."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Nothing to redo" in output

    @patch('builtins.input', side_effect=['add', '5', '3', 'undo', 'redo', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_redo_command_success(self, mock_stdout, mock_input):
        """Test successful redo operation."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Operation redone" in output

    @patch('builtins.input', side_effect=['save', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_save_command_success(self, mock_stdout, mock_input):
        """Test save command saves history successfully."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "History saved successfully" in output

    @patch('builtins.input', side_effect=['save', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_save_command_error(self, mock_stdout, mock_input):
        """Test save command handles errors."""
        with patch('app.calculator.Calculator.save_history', side_effect=Exception("Save failed")):
            calculator_repl()
            output = mock_stdout.getvalue()
            assert "Error saving history" in output

    @patch('builtins.input', side_effect=['load', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_command_success(self, mock_stdout, mock_input):
        """Test load command loads history successfully."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "History loaded successfully" in output

    @patch('builtins.input', side_effect=['load', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_command_error(self, mock_stdout, mock_input):
        """Test load command handles errors."""
        with patch('app.calculator.Calculator.load_history', side_effect=Exception("Load failed")):
            calculator_repl()
            output = mock_stdout.getvalue()
            assert "Error loading history" in output

    @patch('builtins.input', side_effect=['add', '5', '3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_operation(self, mock_stdout, mock_input):
        """Test addition operation."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Result: 8" in output

    @patch('builtins.input', side_effect=['subtract', '10', '3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_subtract_operation(self, mock_stdout, mock_input):
        """Test subtraction operation."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Result: 7" in output

    @patch('builtins.input', side_effect=['multiply', '4', '5', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_multiply_operation(self, mock_stdout, mock_input):
        """Test multiplication operation."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Result: 20" in output

    @patch('builtins.input', side_effect=['divide', '10', '2', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_divide_operation(self, mock_stdout, mock_input):
        """Test division operation."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Result: 5" in output

    @patch('builtins.input', side_effect=['power', '2', '3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_power_operation(self, mock_stdout, mock_input):
        """Test power operation."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Result: 8" in output

    @patch('builtins.input', side_effect=['root', '16', '2', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_root_operation(self, mock_stdout, mock_input):
        """Test root operation."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Result: 4" in output

    @patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_cancel_first_operand(self, mock_stdout, mock_input):
        """Test cancelling operation at first operand."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Operation cancelled" in output

    @patch('builtins.input', side_effect=['add', '5', 'cancel', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_cancel_second_operand(self, mock_stdout, mock_input):
        """Test cancelling operation at second operand."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Operation cancelled" in output

    @patch('builtins.input', side_effect=['divide', '5', '0', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_validation_error(self, mock_stdout, mock_input):
        """Test that ValidationError is caught and displayed."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Error:" in output

    @patch('builtins.input', side_effect=['add', 'invalid', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_unexpected_error_in_operation(self, mock_stdout, mock_input):
        """Test that unexpected errors during operation are caught."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Error:" in output
    @patch('builtins.input', side_effect=['unknown_command', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_unknown_command(self, mock_stdout, mock_input):
        """Test that unknown commands display appropriate message."""
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Unknown command: 'unknown_command'" in output
        assert "Type 'help' for available commands" in output

    @patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_keyboard_interrupt(self, mock_stdout, mock_input):
        """Test that Ctrl+C is handled gracefully."""
        call_count = [0]
        
        def input_side_effect(prompt):
            call_count[0] += 1
            if call_count[0] == 1:
                raise KeyboardInterrupt()
            return 'exit'
        
        mock_input.side_effect = input_side_effect
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Operation cancelled" in output
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_eof_error(self, mock_stdout, mock_input):
        """Test that EOF (Ctrl+D) is handled gracefully."""
        mock_input.side_effect = EOFError()
        calculator_repl()
        output = mock_stdout.getvalue()
        assert "Input terminated. Exiting..." in output
        
    def test_fatal_error_during_initialization(self):
        """Test that fatal errors during initialization are raised."""
        with patch('app.calculator.Calculator', side_effect=Exception("Fatal init error")):
            with pytest.raises(Exception, match="Fatal init error"):
                calculator_repl()
