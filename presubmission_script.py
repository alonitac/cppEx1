import os
import sys
import subprocess
# import os,sys,inspect
# currentdir = os.path.dirname(os.path.abspath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir)
from path import *

EXTRACT_cmd = 'tar -xvf '
README = " README "
REMOVE = lambda x: os.system("rm -f "+x)
FD3 = ">&3"
CS_RULES = 46




def prepare_total_results(readme=None):
    prind_msg = ""
    assert (set(total_number_of_tests.keys()) == set(number_of_failed_tests.keys()))
    if readme is not None:
        prind_msg += ("".join(readme)).replace('\n',"#")+"*"
    for k in number_of_failed_tests:
        prind_msg += k + '#' + str(number_of_failed_tests[k]) + " " + str(total_number_of_tests[k]) + '#'
    return prind_msg


def find_mistake_and_print_input(school_out_p, students_solution, instructions_p, path, memmory_leaks=False, print_memory_leaks=True):
    res, return_values_error = 0, 0
    #test_input = instructions_p.split('#')[1:-1]
    #temp_test_name = os.path.join(test_dir, 'NumericalAnalyzer.c')
    #print(test_input)
    test_input = ''.join(load_data(instructions_p))
    #school_lines = [l[:-1] for l in load_data(school_out_p)]
    #school_out, school_return_code = FACTOR_DATA(school_lines)


    C_SCHOOL_SOLUTION = os.path.join(path, 'FractalDrawerSchool')
    C_STUDENT_SOLUTION = os.path.join(path, 'FractalDrawerStudent')

    # out, err, p = run_test_get_result(C_SCHOOL_SOLUTION, test_path, '000','argument')

    student_out, student_err, st_p = run_test_get_result(C_SCHOOL_SOLUTION, school_out_p, '000','argument')
    school_out, school_err, sc_p = run_test_get_result(C_STUDENT_SOLUTION, school_out_p, '000','argument')

    student_out, student_err, st_p=student_out.split('\n'), student_err.split('\n'), st_p
    school_out, school_err, sc_p=school_out.split('\n'), school_err.split('\n'), sc_p
    #
    # #student_return_code = (student_out.strip() + student_err.strip()).split('\n'), p
    # if ('Assertion' in school_out):
    #     os.system("cp -afr " + os.path.join(path,'IntegerFactorization_ORIGINAL') + ' ' + os.path.join(path,'IntegerFactorization'))
    #
    # else:
    #     os.system("cp -afr " + os.path.join(path,'IntegerFactorization_SCHOOL') + ' ' + os.path.join(path,'IntegerFactorization'))
    #
    # C_SCHOOL_SOLUTION = os.path.join(path, 'IntegerFactorization')
    # student_out, student_err, p = run_test_get_result(C_SCHOOL_SOLUTION, '#', instructions_p)
    # student_out, student_return_code = (student_out.strip() + student_err.strip()).split('\n'), p
    # student_out = [l for l in student_out if l]


    if any(['Assertion' in l for l in school_out]):
        if student_out:
            if not ('Assertion' in student_out[0]):
                print("  >> >> ERROR: You (probably) got wrong in following test: Assertion  << <<  ")
                print_error(test_input, school_out[0], student_out[0])
                return_values_error += 1
                res += 1
        else:
            print("  >> >> ERROR: You (probably) got wrong in following test: Assertion  << <<  ")
            print_error(test_input, school_out, student_out)
            return_values_error += 1
            res += 1
    else:
        if (sc_p != st_p):
            print("  >> >> ERROR: You (probably) got wrong in following test, returncode:  << <<  ")
            print_error(test_input, sc_p, st_p)
            return_values_error = 1

        if len(school_out) != len(student_out):
            print("  >> >> ERROR: You (probably) got wrong in following test, number of lines:  << <<  ")
            print_error(test_input, str(len(school_out)), str(len(student_out)))
            res += 1

        # for i, (row_school, row_student) in enumerate(zip(school_out[-2:], student_out[-2:])):
        #     try:
        #         arr1 = row_school.split('=')[1].split('*')
        #         arr2 = row_student.split('=')[1].split('*')
        #         arr1.sort()
        #         arr2.sort()
        #     except:
        #         arr1=''
        #         arr2='^'
        #     if not arr1==arr2:
        #         print("  >> >> ERROR: You (probably) got wrong in following test, line: " + str(len(student_out[:-2])+i+1) + " : << <<  ")
        #         print_error(test_input, row_school, row_student)
        #         return_values_error += 1
        #         res = 1
        #         break

        for i, (row_school, row_student) in enumerate(zip(school_out, student_out)):
            if (row_school.strip() != row_student.strip()):
                print("  >> >> ERROR: You (probably) got wrong in following test, line: " + str(i) + " : << <<  ")
                print_error(test_input, row_school, row_student)
                res += 1

        # for i , (row_school, row_student) in enumerate(zip(school_out[:-2], student_out[:-2])):
        #     row_school, row_student = PROCESS_LINE(row_school), PROCESS_LINE(row_student)
        #     if (type(row_school) is float) and (type(row_school) is float):
        #         if not ((abs(row_school-row_student)< EPSILON) or (len(str(int(row_school)))>6 and int(row_school)==int(row_student))):
        #
        #             print("  >> >> ERROR: You (probably) got wrong in following test, line: " + str(i) + " : << <<  ")
        #             print_error(test_input, row_school, row_student)
        #
        #             res = +1
        #             break
        #     else:
        #         if (row_school.strip() != row_student.strip()):
        #             print("  >> >> ERROR: You (probably) got wrong in following test, line: " + str(i) + " : << <<  ")
        #             print_error(test_input, row_school, row_student)
        #
        #             res = +1
        #             break


    if memmory_leaks:
        student_out, student_err, p = run_test_get_result('valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose '+C_STUDENT_SOLUTION, school_out_p, '000','argument')
        if 'All heap blocks were freed -- no leaks are possible' in student_err:
            memmory_leak = 0
        else:
            memmory_leak = 1
            if print_memory_leaks:
                print("  >> >> ERROR: You (probably) got memory leak in following test:")
                print_error(test_input, 'All heap blocks were freed -- no leaks are possible', student_err)

        return res, return_values_error, memmory_leak
    else:
        return res, return_values_error, 0




if __name__ == '__main__':
    res = 0
    number_of_failed_tests = {}
    total_number_of_tests = {}
    error_output = []

    def write_results(k, res, total=1):
        if res >0:
            error_output.append(' '+k)
        #
        number_of_failed_tests[k] = number_of_failed_tests.setdefault(k, 0) + res
        total_number_of_tests[k] = total_number_of_tests.setdefault(k, 0) + max(res, total)
        return 0


    if not (len(sys.argv) == 2):
        print("  >> >> ERROR: Tar file was not submitted well                ")
        res = -1
        res = write_results("PRESUBMISSION", 1)
    else:
        tar_path = sys.argv[1]
        if (os.path.dirname(os.path.abspath(__file__)) == '/cs/usr/mick.kab/Documents/C_C++/'+EX+'/final_submission') or \
            (os.path.dirname(os.path.abspath(__file__)) == '/cs/usr/mick.kab/Documents/C_C++/'+EX+'/presubmission'):
            path = os.path.dirname(os.path.abspath(__file__))#os.path.dirname(tar_path)#""
        else:
            path = os.path.join(os.path.dirname(tar_path), 'testdir')
            # os.path.dirname(tar_path)#""
        #print(os.listdir(os.path.dirname(os.path.abspath(__file__))))
        #path = ""  # os.path.join(os.path.dirname(tar_path),

        exe_err_res = 0
        try:
            print("  || || Started untaring files drom tar file: ...               ")

            # #MAKEFILE

            # REMOVE(os.path.join(path,MAKE_FILE[1:-1]))
            # readme_cmd = EXTRACT_cmd+tar_path+MAKE_FILE+"-C "+path
            # std_out, std_err, makefile_err= call(readme_cmd.split(' '))
            os.system("cp -afr " + 'Makefile' + ' ' + path)  ##
            makefile_err = 0

            # if(makefile_err!=0):
            #     print("  >> >> ERROR: Makefile file doesn't exists in the tar file  << <<  ")
            #     res = 1
            # res=write_results("PRESUBMISSION", res)

            #README
            readme_cmd = EXTRACT_cmd + tar_path + README + "-C " + path
            std_out, std_err, readme_err = call(readme_cmd.split(' '))
            readme_err = readme_err.returncode
            if (readme_err != 0):
                print("  >> >> ERROR: README file doesn't exists in the tar file  << <<  ")
                res = 1
            res = write_results("PRESUBMISSION", res)

            # C Files
            for c_file in C_FILES:
                REMOVE(os.path.join(path,c_file))
                exe_cmd = EXTRACT_cmd+tar_path+" "+c_file+" -C "+os.path.join(path,c_file)
                std_out, std_err, exe_err = call(exe_cmd.split(' '))
                exe_err = exe_err.returncode
                res = 0
                if(exe_err!=0):
                    print("  >> >> ERROR: "+c_file+" file doesn't exists in the tar file     ")
                    res = 1
                exe_err_res +=res
                exe_err = write_results("PRESUBMISSION", res)


            if readme_err==0 and exe_err_res==0:
                print("  || || DONE: Untaring. The files were untared well!            ")
            else:
                print("  >> >> ERROR: Makefile or README or "+c_file+" files were untared badly!       ")
            #print(os.listdir(os.path.join(path)))
            #print(os.listdir(os.path.dirname(os.path.abspath(__file__))))
        except Exception as e:
            print("  >> >> ERROR: please SEND e-mail to the course  (CODE 0)    ")


        try:
            #README parsing
            g_res = 0
            readme_arr = []
            with open(os.path.join(path,README[1:-1]), 'r') as readme_f:
                try:
                    readme_arr = readme_f.readlines()
                    if not readme_arr:
                        print("  >> >> ERROR: The README file is empty                             ")
                        res = 1
                    g_res += res
                    res = write_results("README", res)

                    if not (readme_arr[0][:-1]==EX):
                        print("  >> >> ERROR: In README the name of exercise isn't correct         ")
                        print("        Expected '"+EX+"' but got '"+readme_arr[0][:-1]+"'        ")
                        res = 1
                    g_res += res
                    res = write_results("README", res)

                    if not all([l in "qwertyuiopLKJHGFDSAasdfghjklZXCVBNMmnbvcxzasdfghjklQWERTPOIUY_.0123456789" for l in set(readme_arr[1][:-1])]):
                        print("  >> >> ERROR: In README the username is notvalid               ")
                        res = 1
                    g_res += res
                    res = write_results("README", res)

                    if not (all([l in "0123456789" for l in set(readme_arr[2][:-1])]) and len(readme_arr[2][:-1])<=9):
                        print("  >> >> ERROR: In README the ID number is notvalid              ")
                        res = 1
                    g_res += res
                    res = write_results("README", res)

                    if not ((readme_arr[3][:-1]).startswith('#') and (readme_arr[3][:-1]).endswith('#')):
                        print("  >> >> ERROR: In README the '########' line is missing              ")
                        res = 1
                    g_res += res
                    res = write_results("README", res)

                    if not g_res:
                        print("  || || DONE: testing README file!                              ")

                except:
                    print("  >> >> ERROR: testing README file!                           ")

        except Exception as e:
            print("  >> >> ERROR: please SEND e-mail to the course  (CODE 1)   ")
        readme_arr = readme_arr[:3]
        #Coding style
        try:

            if not exe_err_res:
                for c_file in C_FILES:

                    codingstyle_cmd = "bash "+os.path.join(path,"www/codingStyleCheck ") + os.path.join(path, c_file)
                    std_out, std_err,codingstyle_err = call(codingstyle_cmd.split(' '))
                    codingstyle_err = codingstyle_err.returncode

                    if codingstyle_err != 0:
                        print("  >> >> ERROR: Coding style test couldn't run on "+c_file+" well   ")
                    else:
                        coding_style_out = std_out.decode("UTF-8").split('\n')[:-1][-3:]
                        if (int(coding_style_out[-1].split(": ")[-1]) == 0) and \
                           (int(coding_style_out[-2].split(": ")[-1]) == 0) and \
                           (int(coding_style_out[-3].split(": ")[-1]) == 0):
                            print("  || || DONE: coding style test on "+c_file+" passed!                ")
                        else:
                            print("  >> >> ERROR: Coding style test failed on "+c_file+" report:     ")
                            print("            Coding style REPORT:               ")
                            print(std_out.decode("UTF-8"))
                        write_results('CODING_STYLE_RULES', int(coding_style_out[-3].split(": ")[-1]), CS_RULES)
        except:
            print("  >> >> ERROR: please SEND e-mail to the course  (CODE 2)   ")

        #COMPILING
        compile_err = 0

        try:

            if (not exe_err_res) and (not makefile_err):

                if USE_MAKEFILE:
                    clean = os.system('cd '+path+'; make clean')##
                    containes_before = os.listdir(os.path.dirname(os.path.abspath(__file__))) if (path=='') else os.listdir(path)

                    #MAKE
                    make = os.system('cd '+path+'; make;')##
                    res1 = GET_RES(make)
                    containes_now = os.listdir(os.path.dirname(os.path.abspath(__file__))) if (path=='') else os.listdir(path)

                    res1 += IS_COMPILED_WELL(containes_now)

                    #CLEAN
                    clean = os.system('cd '+path+'; make clean;')##
                    res2 = GET_RES(make)
                    containes_after = os.listdir(path)
                    res2 += IS_CLEAN(containes_before, containes_after)

                    #TOTAL
                    compile_err += res1 + res2
                    res1 = write_results("MAKE_COMPILATION", res1)
                    res2 = write_results("MAKE_CLEAN", res2)



                else:
                    #compiling the c file
                    student_solution = os.path.join(path,EX)
                    res = compile_code(path_c_files=path,path_external_files=os.path.dirname(os.path.abspath(__file__)), target=student_solution)
                    compile_err += res
                    res = write_results("COMPILATION", res)
            else:
                compile_err = 1
        except Exception as e:
            print("  >> >> ERROR: please SEND e-mail to the course  (CODE 3)   ")

        try:
            gres = 0
            return_value_err_g = 0
            test_err = 0
            memmory_leaks = 0
            g_memmory_leaks = 0
            if not compile_err:
                os.system('cd ' + path + '; make clean;')
                os.system('cd ' + path + '; make;')
                os.system("cp -afr " + os.path.join(path, 'FractalDrawer') + ' ' + os.path.join(path,'FractalDrawerStudent'))
                os.system('cd ' + path + '; make clean;')

                if (os.path.dirname(
                        os.path.abspath(__file__)) == '/cs/usr/mick.kab/Documents/C_C++/' + EX + '/final_submission') or \
                        (os.path.dirname(
                            os.path.abspath(__file__)) == '/cs/usr/mick.kab/Documents/C_C++/' + EX + '/presubmission'):
                    os.system(
                        "cp -afr " + '/cs/usr/mick.kab/Documents/C_C++/' + EX + '/submission/FractalDrawerSchool' + ' ' + os.path.join(
                            path, 'FractalDrawerSchool'))
                else:
                    os.system(
                        "cp -afr " + 'FractalDrawerSchool' + ' ' + os.path.join(
                            path, 'FractalDrawerSchool'))

                tests_dir = 'tests'
                special_solution = ''
                # os.system("cp -afr " + 'Makefile' + ' ' + path)  ##

                for test_type in os.listdir(tests_dir):
                    test_dir = os.path.join(tests_dir, test_type)
                    in_tests = [f for f in os.listdir(test_dir) if f.endswith('.in')]
                    for test in in_tests:

                        print_m_l = g_memmory_leaks <= 10
                        test_err, return_value_err, memmory_leaks = find_mistake_and_print_input(os.path.join(test_dir, test[:-3]+".out"), \
                                                                                                 special_solution, \
                                                                                  os.path.join(test_dir, test), path, memmory_leaks=MEMMORY_TEST, print_memory_leaks=print_m_l)
                        res += test_err
                        return_value_err_g+=return_value_err
                        gres+=test_err
                        gres+=return_value_err_g
                        # if test_type=='NOT_VALID' and test_err==1:
                        #     print("SHALOM")
                        res = write_results(test[:-3], test_err)
                        return_value_err_g = write_results(test[:-3]+'_RETURNCODE', return_value_err)
                        memmory_leaks = write_results('MEMMORY_LEAKS', memmory_leaks)

                if g_memmory_leaks >0:
                    print("  >> >> ERROR: Testing: got "+str(g_memmory_leaks)+" tests with memmory leaks!                ")
                    print("  || || NOW: Find the leaks in your code!                              ")

                else:
                    print("  || || DONE: Testing: all tests passed well without leaks!                              ")

                if gres >0:
                    print("  >> >> ERROR: Testing: got "+str(gres)+" errors!                ")
                    print("  || || NOW: Find the bugs in your code!                              ")

                else:
                    print("  || || DONE: Testing: all tests passed well!                              ")
                    print("  || || NOW: Try to think about edge cases, which not covered by those tests                              ")

        except Exception as e:
            print("  >> >> ERROR: please SEND e-mail to the course  (CODE 4)    ")
        write_results('FINISHED',1)

        try:
            f= open(3,'w')
            f.write('\n'.join(error_output))
            f.close()
        except:
            print(prepare_total_results(readme_arr))
