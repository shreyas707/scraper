class City < ActiveRecord::Base

	has_many :areas

	validates_uniqueness_of :name
	validates_presence_of :name

end