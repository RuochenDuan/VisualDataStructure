# utils/dsl_parser.py


class DSLParser:
    """
    解析DSL命令
    """
    def __init__(self):
        self.keywords = {
            'create', 'insert', 'delete', 'search', 'help'
        }
        self.struct_types = {
            'alist', 'nlist', 'stck', 'bt', 'bst', 'huff'
        }

    def parse(self, dsl_text: str) -> list[dict]:
        """
        将DSL原始字符串打包为字典列表
        """
        commands = []
        raw_commands = [cmd.strip() for cmd in dsl_text.split(';') if cmd.strip()]
        
        for cmd in raw_commands:
            parsed_cmd = self._parse_command(cmd)
            if parsed_cmd:
                commands.append(parsed_cmd)
        return commands

    def _parse_command(self, cmd: str) -> dict:
        parts = cmd.split()
        if not parts:
            return {}
        command = parts[0].lower()

        result = {
            'command': command,
            'args': [],
            'options': {},
            'flags': []
        }

        i = 1
        while i < len(parts):
            part = parts[i]
            if part.startswith('--'):
                flag = part[2:]
                result['flags'].append(flag)
                i += 1
            elif part.startswith('-'):
                option = part[1:]
                result['options']['struct_type'] = option
                if i + 1 < len(parts) and not parts[i+1].startswith('-'):
                    i += 1
                    args_str = parts[i]
                    result['args'] = self._parse_args(args_str)
                else:
                    result['args'] = []
                i += 1
            else:
                result['args'].extend(self._parse_args(part))
                i += 1
        return result

    def _parse_args(self, args_str: str) -> list:
        if not args_str:
            return []

        args = [arg.strip() for arg in args_str.split(',') if arg.strip()]
        parsed_args = []
        for arg in args:
            try:
                if '.' in arg:
                    parsed_args.append(float(arg))
                else:
                    parsed_args.append(int(arg))
            except ValueError:
                parsed_args.append(arg)
        return parsed_args
