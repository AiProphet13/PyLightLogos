import dis
from collections import Counter
from .logos import LightSpeedLogos

def normalize_instruction(instr):
    """Enhanced normalization with argument typing"""
    opname = instr.opname
    arg_type = ""
    
    if "LOAD" in opname:
        if "FAST" in opname: arg_type = "VAR"
        elif "CONST" in opname:
            if isinstance(instr.argval, int): arg_type = "INT"
            elif isinstance(instr.argval, float): arg_type = "FLOAT"
            else: arg_type = "CONST"
        elif "ATTR" in opname: arg_type = "ATTR"
        elif "GLOBAL" in opname: arg_type = "GLOBAL"
        else: arg_type = "NAME"
    elif "STORE" in opname:
        arg_type = "VAR"
    elif "JUMP" in opname:
        arg_type = "LABEL"
    elif "CALL" in opname:
        arg_type = "FUNC"
    elif "COMPARE" in opname:
        arg_type = "OP"
    
    return (opname, arg_type)

def extract_bytecode_patterns(code_string, min_frequency=2):
    """Extract bytecode patterns and create micro-language"""
    try:
        code_obj = compile(code_string, "<string>", "exec")
        instructions = list(dis.get_instructions(code_obj))
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from e

    normalized = [normalize_instruction(i) for i in instructions]
    
    pattern_counter = Counter()
    for n in range(2, 6):  # Analyze 2-5 instruction sequences
        for i in range(len(normalized) - n + 1):
            sequence = tuple(normalized[i:i+n])
            pattern_counter[sequence] += 1

    micro_mapping = {}
    used_instructions = set()
    
    # Sort by frequency and pattern length
    sorted_patterns = sorted(
        pattern_counter.items(), 
        key=lambda x: (x[1], len(x[0])), 
        reverse=True
    )
    
    for pattern, count in sorted_patterns:
        if count >= min_frequency and not any(instr in used_instructions for instr in pattern):
            primitive_name = f"BYTE_MACRO_{len(micro_mapping)+1}"
            micro_mapping[primitive_name] = pattern
            used_instructions.update(pattern)
            if len(micro_mapping) >= 10:  # Limit to top patterns
                break
                
    return micro_mapping, instructions, normalized

def compress_bytecode(instructions, normalized, micro_mapping):
    """Compress bytecode using detected patterns"""
    pattern_map = {pattern: name for name, pattern in micro_mapping.items()}
    patterns_sorted = sorted(pattern_map.keys(), key=len, reverse=True)
    
    compressed = []
    i = 0
    while i < len(normalized):
        matched = False
        for pattern in patterns_sorted:
            end = i + len(pattern)
            if end <= len(normalized) and tuple(normalized[i:end]) == pattern:
                compressed.append(pattern_map[pattern])
                i = end
                matched = True
                break
                
        if not matched:
            op, arg_type = normalized[i]
            arg_val = instructions[i].argval
            compressed.append(instructions[i].opname)
            i += 1
            
    return compressed

def optimize_with_peephole(compressed_stream, optimization_rules=None):
    """Apply second-stage optimization to macro patterns"""
    if optimization_rules is None:
        # Default optimization rules
        optimization_rules = {
            ('BUILD_LIST', 'STORE_FAST', 'SETUP_LOOP', 'GET_ITER'): 'SUPER_MACRO_INIT_LOOP',
            ('BYTE_MACRO_1', 'BYTE_MACRO_1'): 'SUPER_MACRO_DOUBLE_ACCUM',
            ('BYTE_MACRO_2', 'BYTE_MACRO_3'): 'SUPER_MACRO_COND_APPEND'
        }
    
    optimized_stream = []
    rules_sorted = sorted(optimization_rules.items(), key=lambda x: len(x[0]), reverse=True)
    
    i = 0
    while i < len(compressed_stream):
        matched = False
        for pattern, super_macro in rules_sorted:
            end = i + len(pattern)
            if tuple(compressed_stream[i:end]) == pattern:
                optimized_stream.append(super_macro)
                i = end
                matched = True
                break
        
        if not matched:
            optimized_stream.append(compressed_stream[i])
            i += 1
            
    return optimized_stream

def analyze_code(code, min_frequency=2, optimization_rules=None):
    """Complete analysis pipeline for Python code"""
    # Extract bytecode patterns
    micro_ops, instructions, normalized = extract_bytecode_patterns(code, min_frequency)
    
    # First compression pass
    compressed = compress_bytecode(instructions, normalized, micro_ops)
    
    # Peephole optimization
    optimized = optimize_with_peephole(compressed, optimization_rules)
    
    # Generate Light Speed Logos
    logo_generator = LightSpeedLogos()
    logo_stream = logo_generator.visualize(optimized)
    architecture_fingerprint = logo_generator.generate_architecture_fingerprint(logo_stream)
    
    return {
        'original_instructions': [i.opname for i in instructions],
        'compressed': compressed,
        'optimized': optimized,
        'logos': logo_stream,
        'fingerprint': architecture_fingerprint,
        'statistics': {
            'original_length': len(instructions),
            'compressed_length': len(compressed),
            'optimized_length': len(optimized),
            'logo_length': len(logo_stream),
            'compression_ratio': len(logo_stream) / len(instructions) if instructions else 0
        },
        'micro_ops': micro_ops
    }
