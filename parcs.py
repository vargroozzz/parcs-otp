from Pyro4 import expose
import random

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")    

    def expand_key(self, primary_key, n):
        random.seed(primary_key)
        self.key = [random.randrange(0, 256) for _ in range(n)]
     

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        key, self.msg = self.read_input()

        msg_len = len(self.msg)

        self.expand_key(key, msg_len)
        
        step = int(msg_len / len(self.workers))
        
        mapped = []
        for i in range(len(self.workers)):
            print("map %d" % i)
            mapped.append(self.workers[i].map(self.key[(step * i):(step * (i + 1))], self.msg[(step * i):(step * (i + 1))]))

   
        ct = Solver.reduce(mapped)

        self.write_output(ct)

        print("Job Finished")

    @staticmethod
    @expose
    def encrypt(key, msg):
        assert len(key) == len(msg)
        ct = [int(key[i] ^ msg[i]) for i in range(len(key)) ]
        return ct             
   
    @staticmethod
    @expose
    def map(key, msg):
        return Solver.encrypt(key, msg)

    @staticmethod
    @expose
    def reduce(mapped):
        print("Reduce begin")
        output = []
        for ct in mapped:
            output = output + ct.value
        print("Reduce done")
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        lines = f.readlines()
        f.close()

        key = long(lines[0][:-1], 16)
        msg = [int(ord(ch)) for ch in lines[1]]

        return key, msg

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
    
        string = ''.join([chr(byte) for byte in output])
        #for ch in chrs:
        #    f.write(ch)
        f.write(string)
        f.close()
        print("Output done")
