import subprocess

def system(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE).communicate()

LANGUAGE = "Java"
EXT = "java"
VERSION = system(["java", "-version"])[1].split()[2].strip('"')
ADDITIONAL_FILES = []

def setup(sandbox, source_code):
    sandbox.write_file(source_code, "Main.java")
    compiled = sandbox.run("javac Main.java", stdout=".stdout",
                           stderr=".stderr", time_limit=10)
    if compiled.split()[0] != "OK":
        return {"status": "error",
                "message": ("MONITOR:\n" + compiled + "\n" +
                            "STDERR:\n" + sandbox.read_file(".stderr") + "\n" +
                            "STDOUT:\n" + sandbox.read_file(".stdout"))}
    return {"status": "ok"}

def run(sandbox, input_file, time_limit, memory_limit):
    result = sandbox.run("java Main", stdin=input_file, time_limit=time_limit,
                         override_memory_limit=memory_limit,
                         stdout=".stdout", stderr=".stderr")
    toks = result.split()
    if toks[0] != "OK":
        return {"status": "fail", "message": result, "verdict": toks[0] }
    return {"status": "ok", "time": toks[1], "memory": toks[2], "output": ".stdout"}
