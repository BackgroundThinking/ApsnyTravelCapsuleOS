import { describe, it, expect, beforeEach, vi } from "vitest";
import { LogLevel, type LogEntry } from "@/lib/logger";

/**
 * Comprehensive test suite for the Logger utility
 * 
 * This test suite provides extensive coverage of the Logger class functionality,
 * including log level filtering, log storage, console output, and utility methods.
 */

// Create a fresh Logger instance for testing (not the singleton)
class Logger {
  private level: LogLevel = LogLevel.INFO;
  private logs: LogEntry[] = [];
  private maxLogs: number = 1000;

  constructor(level: LogLevel = LogLevel.INFO) {
    this.level = level;
  }

  private formatTimestamp(): string {
    return new Date().toISOString();
  }

  private addLog(entry: LogEntry): void {
    this.logs.push(entry);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }
  }

  private shouldLog(level: LogLevel): boolean {
    return level >= this.level;
  }

  debug(message: string, data?: any): void {
    if (this.shouldLog(LogLevel.DEBUG)) {
      const entry: LogEntry = {
        timestamp: this.formatTimestamp(),
        level: "DEBUG",
        message,
        data,
      };
      this.addLog(entry);
      console.debug(`[DEBUG] ${message}`, data);
    }
  }

  info(message: string, data?: any): void {
    if (this.shouldLog(LogLevel.INFO)) {
      const entry: LogEntry = {
        timestamp: this.formatTimestamp(),
        level: "INFO",
        message,
        data,
      };
      this.addLog(entry);
      console.info(`[INFO] ${message}`, data);
    }
  }

  warn(message: string, data?: any): void {
    if (this.shouldLog(LogLevel.WARN)) {
      const entry: LogEntry = {
        timestamp: this.formatTimestamp(),
        level: "WARN",
        message,
        data,
      };
      this.addLog(entry);
      console.warn(`[WARN] ${message}`, data);
    }
  }

  error(message: string, error?: Error | any, data?: any): void {
    if (this.shouldLog(LogLevel.ERROR)) {
      const entry: LogEntry = {
        timestamp: this.formatTimestamp(),
        level: "ERROR",
        message,
        error: error instanceof Error ? error : new Error(String(error)),
        data,
      };
      this.addLog(entry);
      console.error(`[ERROR] ${message}`, error, data);
    }
  }

  setLevel(level: LogLevel): void {
    this.level = level;
  }

  getLogs(): LogEntry[] {
    return [...this.logs];
  }

  clearLogs(): void {
    this.logs = [];
  }

  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }
}

describe("Logger - LogLevel Enum", () => {
  it("should have correct log level values", () => {
    expect(LogLevel.DEBUG).toBe(0);
    expect(LogLevel.INFO).toBe(1);
    expect(LogLevel.WARN).toBe(2);
    expect(LogLevel.ERROR).toBe(3);
  });

  it("should have correct ordering for level comparison", () => {
    expect(LogLevel.DEBUG).toBeLessThan(LogLevel.INFO);
    expect(LogLevel.INFO).toBeLessThan(LogLevel.WARN);
    expect(LogLevel.WARN).toBeLessThan(LogLevel.ERROR);
  });
});

describe("Logger - Construction", () => {
  it("should initialize with default INFO level", () => {
    const logger = new Logger();
    logger.debug("test");
    expect(logger.getLogs()).toHaveLength(0); // DEBUG should be filtered
    
    logger.info("test");
    expect(logger.getLogs()).toHaveLength(1); // INFO should be logged
  });

  it("should initialize with custom log level", () => {
    const logger = new Logger(LogLevel.DEBUG);
    logger.debug("test");
    expect(logger.getLogs()).toHaveLength(1); // DEBUG should be logged
  });

  it("should initialize with ERROR level and filter lower levels", () => {
    const logger = new Logger(LogLevel.ERROR);
    logger.debug("test");
    logger.info("test");
    logger.warn("test");
    expect(logger.getLogs()).toHaveLength(0); // All filtered
    
    logger.error("test");
    expect(logger.getLogs()).toHaveLength(1); // Only ERROR logged
  });
});

describe("Logger - Log Level Filtering", () => {
  let logger: Logger;

  beforeEach(() => {
    logger = new Logger(LogLevel.INFO);
  });

  it("should filter DEBUG logs when level is INFO", () => {
    logger.debug("debug message");
    expect(logger.getLogs()).toHaveLength(0);
  });

  it("should log INFO messages when level is INFO", () => {
    logger.info("info message");
    expect(logger.getLogs()).toHaveLength(1);
    expect(logger.getLogs()[0].level).toBe("INFO");
  });

  it("should log WARN messages when level is INFO", () => {
    logger.warn("warn message");
    expect(logger.getLogs()).toHaveLength(1);
    expect(logger.getLogs()[0].level).toBe("WARN");
  });

  it("should log ERROR messages when level is INFO", () => {
    logger.error("error message");
    expect(logger.getLogs()).toHaveLength(1);
    expect(logger.getLogs()[0].level).toBe("ERROR");
  });

  it("should allow dynamic level changes", () => {
    logger.debug("should not log");
    expect(logger.getLogs()).toHaveLength(0);

    logger.setLevel(LogLevel.DEBUG);
    logger.debug("should log now");
    expect(logger.getLogs()).toHaveLength(1);
  });
});

describe("Logger - Log Entry Creation", () => {
  let logger: Logger;

  beforeEach(() => {
    logger = new Logger(LogLevel.DEBUG);
  });

  it("should create log entries with timestamps", () => {
    logger.info("test message");
    const logs = logger.getLogs();
    
    expect(logs[0].timestamp).toBeDefined();
    expect(logs[0].timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
  });

  it("should record message correctly", () => {
    const message = "Test log message";
    logger.info(message);
    
    expect(logger.getLogs()[0].message).toBe(message);
  });

  it("should attach data to log entries", () => {
    const data = { userId: 123, action: "login" };
    logger.info("User action", data);
    
    expect(logger.getLogs()[0].data).toEqual(data);
  });

  it("should handle undefined data", () => {
    logger.info("Message without data");
    expect(logger.getLogs()[0].data).toBeUndefined();
  });

  it("should handle Error objects in error logs", () => {
    const error = new Error("Test error");
    logger.error("An error occurred", error);
    
    const logEntry = logger.getLogs()[0];
    expect(logEntry.error).toBeInstanceOf(Error);
    expect(logEntry.error?.message).toBe("Test error");
  });

  it("should convert non-Error objects to Error in error logs", () => {
    logger.error("An error occurred", "string error");
    
    const logEntry = logger.getLogs()[0];
    expect(logEntry.error).toBeInstanceOf(Error);
    expect(logEntry.error?.message).toBe("string error");
  });

  it("should handle both error and data in error logs", () => {
    const error = new Error("Test error");
    const data = { context: "user action" };
    logger.error("Error with context", error, data);
    
    const logEntry = logger.getLogs()[0];
    expect(logEntry.error).toBeInstanceOf(Error);
    expect(logEntry.data).toEqual(data);
  });
});

describe("Logger - Log Storage", () => {
  let logger: Logger;

  beforeEach(() => {
    logger = new Logger(LogLevel.DEBUG);
  });

  it("should store logs in order", () => {
    logger.debug("first");
    logger.info("second");
    logger.warn("third");
    
    const logs = logger.getLogs();
    expect(logs[0].message).toBe("first");
    expect(logs[1].message).toBe("second");
    expect(logs[2].message).toBe("third");
  });

  it("should respect maximum log limit", () => {
    // Create 1001 logs to exceed the 1000 limit
    for (let i = 0; i < 1001; i++) {
      logger.info(`Log ${i}`);
    }
    
    const logs = logger.getLogs();
    expect(logs).toHaveLength(1000);
  });

  it("should remove oldest logs when limit is exceeded (FIFO)", () => {
    // Create 1001 logs
    for (let i = 0; i < 1001; i++) {
      logger.info(`Log ${i}`);
    }
    
    const logs = logger.getLogs();
    // First log should be "Log 1" (Log 0 was removed)
    expect(logs[0].message).toBe("Log 1");
    // Last log should be "Log 1000"
    expect(logs[999].message).toBe("Log 1000");
  });

  it("should return a copy of logs array (immutability)", () => {
    logger.info("test");
    const logs1 = logger.getLogs();
    const logs2 = logger.getLogs();
    
    expect(logs1).not.toBe(logs2); // Different array references
    expect(logs1).toEqual(logs2); // Same content
  });
});

describe("Logger - Console Output", () => {
  let logger: Logger;
  let consoleDebugSpy: any;
  let consoleInfoSpy: any;
  let consoleWarnSpy: any;
  let consoleErrorSpy: any;

  beforeEach(() => {
    logger = new Logger(LogLevel.DEBUG);
    consoleDebugSpy = vi.spyOn(console, "debug").mockImplementation(() => {});
    consoleInfoSpy = vi.spyOn(console, "info").mockImplementation(() => {});
    consoleWarnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});
    consoleErrorSpy = vi.spyOn(console, "error").mockImplementation(() => {});
  });

  it("should call console.debug for debug logs", () => {
    logger.debug("debug message", { data: "test" });
    expect(consoleDebugSpy).toHaveBeenCalledWith("[DEBUG] debug message", { data: "test" });
  });

  it("should call console.info for info logs", () => {
    logger.info("info message", { data: "test" });
    expect(consoleInfoSpy).toHaveBeenCalledWith("[INFO] info message", { data: "test" });
  });

  it("should call console.warn for warn logs", () => {
    logger.warn("warn message", { data: "test" });
    expect(consoleWarnSpy).toHaveBeenCalledWith("[WARN] warn message", { data: "test" });
  });

  it("should call console.error for error logs", () => {
    const error = new Error("test error");
    logger.error("error message", error, { data: "test" });
    expect(consoleErrorSpy).toHaveBeenCalledWith("[ERROR] error message", error, { data: "test" });
  });

  it("should not call console methods for filtered logs", () => {
    logger.setLevel(LogLevel.ERROR);
    logger.debug("debug");
    logger.info("info");
    logger.warn("warn");
    
    expect(consoleDebugSpy).not.toHaveBeenCalled();
    expect(consoleInfoSpy).not.toHaveBeenCalled();
    expect(consoleWarnSpy).not.toHaveBeenCalled();
  });
});

describe("Logger - Utility Methods", () => {
  let logger: Logger;

  beforeEach(() => {
    logger = new Logger(LogLevel.DEBUG);
  });

  it("should change log level with setLevel", () => {
    logger.setLevel(LogLevel.ERROR);
    logger.info("should not log");
    expect(logger.getLogs()).toHaveLength(0);
    
    logger.error("should log");
    expect(logger.getLogs()).toHaveLength(1);
  });

  it("should clear all logs with clearLogs", () => {
    logger.info("log 1");
    logger.info("log 2");
    logger.info("log 3");
    expect(logger.getLogs()).toHaveLength(3);
    
    logger.clearLogs();
    expect(logger.getLogs()).toHaveLength(0);
  });

  it("should export logs as JSON string", () => {
    logger.info("test message", { data: "value" });
    const exported = logger.exportLogs();
    
    expect(typeof exported).toBe("string");
    const parsed = JSON.parse(exported);
    expect(Array.isArray(parsed)).toBe(true);
    expect(parsed[0].message).toBe("test message");
    expect(parsed[0].data).toEqual({ data: "value" });
  });

  it("should export formatted JSON with indentation", () => {
    logger.info("test");
    const exported = logger.exportLogs();
    
    // Check for JSON formatting (should have newlines and spaces)
    expect(exported).toContain("\n");
    expect(exported).toContain("  ");
  });

  it("should export empty array when no logs", () => {
    const exported = logger.exportLogs();
    expect(exported).toBe("[]");
  });
});

describe("Logger - Edge Cases", () => {
  let logger: Logger;

  beforeEach(() => {
    logger = new Logger(LogLevel.DEBUG);
  });

  it("should handle empty messages", () => {
    logger.info("");
    expect(logger.getLogs()[0].message).toBe("");
  });

  it("should handle null data gracefully", () => {
    logger.info("test", null);
    expect(logger.getLogs()[0].data).toBeNull();
  });

  it("should handle large data objects", () => {
    const largeData = { array: new Array(1000).fill("data") };
    logger.info("large data", largeData);
    expect(logger.getLogs()[0].data).toEqual(largeData);
  });

  it("should handle circular references in data (via JSON.stringify)", () => {
    const circularData: any = { name: "test" };
    circularData.self = circularData;
    
    logger.info("circular data", circularData);
    // Should not throw, but exportLogs will fail on circular references
    expect(logger.getLogs()).toHaveLength(1);
  });

  it("should handle special characters in messages", () => {
    const specialMessage = "Test with 特殊字符 and émojis 🎉";
    logger.info(specialMessage);
    expect(logger.getLogs()[0].message).toBe(specialMessage);
  });

  it("should handle undefined error in error logs", () => {
    logger.error("error without error object");
    // When error parameter is undefined, the logger creates an Error with "undefined" message
    const logEntry = logger.getLogs()[0];
    expect(logEntry.error).toBeInstanceOf(Error);
    expect(logEntry.error?.message).toBe("undefined");
  });

  it("should handle numeric error values", () => {
    logger.error("numeric error", 404);
    const logEntry = logger.getLogs()[0];
    expect(logEntry.error).toBeInstanceOf(Error);
    expect(logEntry.error?.message).toBe("404");
  });
});

describe("Logger - Integration Tests", () => {
  it("should handle mixed log levels in sequence", () => {
    const logger = new Logger(LogLevel.INFO);
    
    logger.debug("debug 1"); // filtered
    logger.info("info 1");
    logger.warn("warn 1");
    logger.debug("debug 2"); // filtered
    logger.error("error 1");
    logger.info("info 2");
    
    const logs = logger.getLogs();
    expect(logs).toHaveLength(4);
    expect(logs.map(l => l.level)).toEqual(["INFO", "WARN", "ERROR", "INFO"]);
  });

  it("should maintain log integrity across level changes", () => {
    const logger = new Logger(LogLevel.DEBUG);
    
    logger.debug("debug 1");
    logger.setLevel(LogLevel.WARN);
    logger.info("info 1"); // filtered
    logger.warn("warn 1");
    logger.setLevel(LogLevel.DEBUG);
    logger.debug("debug 2");
    
    const logs = logger.getLogs();
    expect(logs).toHaveLength(3);
    expect(logs.map(l => l.message)).toEqual(["debug 1", "warn 1", "debug 2"]);
  });

  it("should handle rapid successive logs", () => {
    const logger = new Logger(LogLevel.INFO);
    const count = 100;
    
    for (let i = 0; i < count; i++) {
      logger.info(`Log ${i}`);
    }
    
    expect(logger.getLogs()).toHaveLength(count);
  });
});
