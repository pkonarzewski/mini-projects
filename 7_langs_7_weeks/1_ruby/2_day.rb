def tell_the_truth
    true
end

puts tell_the_truth

# arrays
# [] is method of array
# arrays dont need to be homogeneous

animals = ['cat', 'dog', 'snake']
puts animals

puts animals[0], animals[-1], animals[0..1]

puts animals[10]

puts ((0..1).class)


# Hash
# like dicts in Python

numbers = {1 => 'one', 2 => 'two'}
puts numbers[1]

# symbols
aaa = {:array=>[1, 2, 3], :string=>"Hi, mom!"}
puts aaa[:string]

# there is no named parameters, but u cane use hashes

def tell_the_truth(options={})
    if options[:profession] == :lawyer
        'i cant'
    else
        true
    end
end

puts tell_the_truth
puts tell_the_truth :profession => :lawyer

# Code Blocks
# function without a name

3.times {puts 'write me down'}

animals = ['lions and ', 'tigers and', 'bears', 'oh my']
animals.each {|a| puts a}
# code block is between {}

# adds method to existing class
class Integer
    def my_times
        i = self
        while i > 0
            i = i - 1
            yield
        end
    end
end

puts 3.class
3.my_times {puts 'mango moose'}

# blocks can be first-class parameters
def call_block(&block)
    block.call
end

def pass_block(&block)
    call_block(&block)
end

pass_block {puts 'Hello, block'}
# can be used to
# delay execution
# conditional execution
# enforce policy


# Classes
puts 4.class
puts 4.class.superclass
puts 4.class.superclass.superclass
puts 4.class.superclass.superclass.superclass

puts 4.class.class
puts 4.class.class.superclass
puts 4.class.class.superclass.superclass


# Class Tree
class Tree
    attr_accessor :children, :node_name

    def initialize(name, children=[])
        @children = children
        @node_name = name
    end

    def visit_all(&block)
        visit &block
        children.each{|c| c.visit_all &block}
    end

    def visit(&block)
        block.call self
    end
end

ruby_tree = Tree.new("Ruby", [Tree.new("Reia"), Tree.new("MacRuby")])

puts "=Visiting a node"
ruby_tree.visit{|node| puts node.node_name}

puts "=Visit entire tree"
ruby_tree.visit_all {|node| puts node.node_name}

# Class conventions
# class name CamelCase
# @ is instance variable
# @@ is class variable
# other underscore style
# constant ALL_CAPS
# atr define instance variable


# Mixin
# modules is collection of functions and constants

module ToFile
    def filename
        "object #{self.object_id}.txt"
    end

    def to_f
        File.open(filename, 'w') {|f| f.write(to_s)}
    end
end

class Person
    include ToFile
    attr_accessor :name

    def initialize(name)
        @name = name
    end

    def to_s
        name
    end
end

Person.new('matz').to_f
