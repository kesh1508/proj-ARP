CC = gcc
RM = rm

CFLAGS = -O2 -Wall -c

OUTPUT_DIR = bin
OBJ_DIR = obj

TARGET_LIB = $(OUTPUT_DIR)/calculator

INCLUDES = \
    -I/usr/include/python3.11  # Updated to Python 3.11

LIB_SRCS = calculator.c
LIB_OBJS  = $(LIB_SRCS:%.c=$(OBJ_DIR)/%.o)

.PHONY: all
all: $(TARGET_LIB)

$(TARGET_LIB): $(LIB_OBJS)
	mkdir -p $(dir $@)
	$(CC) -shared $^ $(INCLUDES) -o $@.so

$(OBJ_DIR)/%.o: %.c
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@

.PHONY: clean
clean:
	-$(RM) -rf $(OUTPUT_DIR)/* $(OBJ_DIR)/*

