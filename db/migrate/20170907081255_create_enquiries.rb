class CreateEnquiries < ActiveRecord::Migration
  def change
    create_table :enquiries do |t|
      t.string :title
      t.string :name
      t.date :date
      t.string :status
      t.string :location_preference
      t.string :link
      t.integer :area_id
      t.integer :category_id

      t.timestamps null: false
    end
  end
end
