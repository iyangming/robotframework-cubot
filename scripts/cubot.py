#! /usr/bin/env python
from robot.api import TestSuite
from robot.api import TestSuiteBuilder
from robot.api import ResourceFile
from robot.api import ResultWriter
import os.path
import glob


def read_feature(filename):
    print '=' * 78
    print 'Parsing feature: %s' % filename
    print '=' * 78
    keywords = []

    file_feature = os.path.splitext(os.path.basename(filename))[0]
    my_resource = filename.replace('.feature', '.txt' )
    
    if not os.path.exists(my_resource):
        my_resource = filename.replace('.feature', '.html' )
        if not os.path.exists(my_resource):
            print "\033[1;31;40mWARNING:\033[1;37;40m No resource file for this feature (%s.[txt|html])\033[0m" % file_feature
            my_resource = None

    suite = TestSuite(file_feature)
    suite.imports.library('OperatingSystem')
    
    if my_resource:
        #print 'Found keywords:'
        resource = ResourceFile(my_resource).populate()
        for k in resource.keywords:
            #print ' %s' % k.name
            keywords.append(k.name.lower())
            

        suite.imports.resource(my_resource)
        #print '-' * 78
    #else:
    #    resource = ResourceFile(filename.replace('.feature', '.html' ))

    #print keywords

    in_scenario = False
    lineno = 0
    cnt_steps = 0
    undefined_steps = []

    f = open( filename, 'r' )
    for line in f:
        lineno += 1
        if line.strip():
            l = line.strip()
            if line[:8] == 'Feature:':
                print "\033[1;37;40m%s\033[0m" % line.rstrip()

            elif l[:9] == 'Scenario:':
                print "\033[1;37;40m%s\033[0m" % line.rstrip()
                current_scenario = l[9:].strip()
                test = suite.tests.create(current_scenario)
                in_scenario = True

            elif in_scenario:
                test_step = l.strip()
                cnt_steps += 1
                test_step2 = test_step

                if test_step.split(' ')[0] in ['Given','When','Then']:
                    test_step2 =  ' '.join(test_step.split(' ')[1:])

                test.keywords.create( test_step )
                print ' ' * 6,
                if test_step.lower() in keywords or test_step2.lower() in keywords:
                    print "\033[1;30;40m",
                else:
                    print "\033[33;40m",
                    if not test_step2 in undefined_steps:
                        undefined_steps.append(test_step2)
                    
                    #kw = UserKeyword( resource, test_step2 )


                filler = ' ' * (40 - len(test_step))
                print "%s%s%s:%d\033[0m" % (test_step, filler, filename, lineno)

            else:
                print line,

    if undefined_steps:
        #resource.save()
        print ""
        print "Undefined keywords:"
        for k in undefined_steps:
            print k
        print
        print "These keywords can already be defined, but have variables in the name"
        print "or be available in a deeper resource file"
        print

    return suite

def execute(suite):
    ## execute
    print '=' * 78
    print 'Run test'
    #print '=' * 78
    return suite.run( output='output.xml' )

    

def report(result):
    # Report and xUnit files can be generated based on the  result object.
    ResultWriter(result).write_results(report='report.html', xunit='xunit.xml', log=None)

if __name__ == '__main__':
    

    file_list = glob.glob('*.feature')
    init_suite = None
    if os.path.exists( '__init__.txt' ):
        print "__init__ found"
        init_suite = TestSuiteBuilder().build('__init__.txt')

    if len(file_list)==0:
        import sys
        print "No feature files found."
        sys.exit()

    elif len(file_list) > 1:
        suite = TestSuite('Main')
        if init_suite:
            suite.suites.append( init_suite )

        for f in file_list:
            feature_suite = read_feature( f )
            suite.suites.append( feature_suite )
    
    else:
        if init_suite:
            suite = TestSuite('Main')
            suite.suites.append( init_suite )
            feature_suite = read_feature( file_list[0] )
            suite.suites.append( feature_suite )

        else:
            suite = read_feature( file_list[0] )
    
    
    result = execute( suite )

    report(result)


    ## report


