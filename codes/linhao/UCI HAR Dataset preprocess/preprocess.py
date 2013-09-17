import re

############generate weka train data######################
path = 'train'
feature_vector_file = open('%s/%s'%(path,'X_train.txt'),'r')
class_label_file = open('%s/%s'%(path,'y_train.txt'),'r')
train_data_file = open('hao_train_data.arff','w')

feature_vector_lines = feature_vector_file.readlines()
class_label_lines = class_label_file.readlines()

#write arff header
train_data_file.write('@relation uci_har_train_data\n')
for i in range(1,561+1):
	train_data_file.write('@attribute feature%d numeric\n' % i)

train_data_file.write('@attribute class_label {1,2,3,4,5,6}\n')
train_data_file.write('@data\n')

#fill in data
for i in range(0,len(class_label_lines)):
	feature_vector_line_processed, times = re.subn(' +',',',feature_vector_lines[i].strip())
	train_data_file.write('%s,%s\n' % (feature_vector_line_processed, class_label_lines[i].strip()))

feature_vector_file.close()
class_label_file.close()
train_data_file.close()


############generate weka test data######################
path = 'test'
feature_vector_file = open('%s/%s'%(path,'X_test.txt'),'r')
class_label_file = open('%s/%s'%(path,'y_test.txt'),'r')
test_data_file = open('hao_test_data.arff','w')

feature_vector_lines = feature_vector_file.readlines()
class_label_lines = class_label_file.readlines()

#write arff header
test_data_file.write('@relation uci_har_test_data\n')
for i in range(1,561+1):
	test_data_file.write('@attribute feature%d numeric\n' % i)

test_data_file.write('@attribute class_label {1,2,3,4,5,6}\n')
test_data_file.write('@data\n')

#fill in data
for i in range(0,len(class_label_lines)):
	feature_vector_line_processed, times = re.subn(' +',',',feature_vector_lines[i].strip())
	test_data_file.write('%s,%s\n' % (feature_vector_line_processed, class_label_lines[i].strip()))

feature_vector_file.close()
class_label_file.close()
test_data_file.close()
