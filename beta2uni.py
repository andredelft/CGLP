from Tools.uni_beta_code import beta2uni
import sys

if __name__ == '__main__':
   beta_code = ' '.join(sys.argv[1:])
   print(beta2uni(beta_code))
